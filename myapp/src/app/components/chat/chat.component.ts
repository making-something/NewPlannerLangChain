import { Component, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PlannerService } from '../../services/planner.service';
import { MarkdownPipe } from '../../pipes/markdown.pipe';
import { Subscription } from 'rxjs';
import { 
  ItineraryRequest, 
  ItineraryResponse, 
  ProviderInfo, 
  ModelItem, 
  FollowUpQuestion,
  RefinementRequest
} from '../../models/planner.models';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  followUpQuestions?: FollowUpQuestion[];
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownPipe],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  providers: ProviderInfo[] = [];
  selectedProvider: string = 'cerebras';
  selectedModel: string = 'llama-3.3-70b';
  
  userInput: string = '';
  messages: Message[] = [];
  isLoading: boolean = false;
  sessionId: string | null = null;
  private resetSubscription: Subscription | undefined;

  // Templates for the welcome screen
  templates = [
    { icon: '✈️', title: 'Plan a 3-day trip', desc: 'A 3-day trip to see the northern lights in Norway...' },
    { icon: '💡', title: 'Help me find the best place for me ', desc: 'what are best places for a ...' },
    { icon: '🎁', title: 'Help me pick', desc: 'Here are some ideas for ...' }
  ];

  constructor(private plannerService: PlannerService) {}

  ngOnInit(): void {
    this.loadModels();
    this.resetSubscription = this.plannerService.resetChat$.subscribe(() => {
      this.resetChat();
    });
  }

  ngOnDestroy(): void {
    if (this.resetSubscription) {
      this.resetSubscription.unsubscribe();
    }
  }

  resetChat(): void {
    this.messages = [];
    this.sessionId = null;
    this.userInput = '';
    this.isLoading = false;
  }

  loadModels(): void {
    this.plannerService.getModels().subscribe({
      next: (response) => {
        this.providers = response.providers;
        if (this.providers.length > 0) {
          // Default to first provider/model if not set
          // But we want to default to Cerebras as per code
          const cerebras = this.providers.find(p => p.provider === 'cerebras');
          if (cerebras) {
            this.selectedProvider = 'cerebras';
            this.selectedModel = cerebras.models[0].id;
          } else {
            this.selectedProvider = this.providers[0].provider;
            this.selectedModel = this.providers[0].models[0].id;
          }
        }
      },
      error: (err) => console.error('Failed to load models', err)
    });
  }

  get currentModels(): ModelItem[] {
    const provider = this.providers.find(p => p.provider === this.selectedProvider);
    return provider ? provider.models : [];
  }

  onProviderChange(): void {
    const provider = this.providers.find(p => p.provider === this.selectedProvider);
    if (provider && provider.models.length > 0) {
      this.selectedModel = provider.models[0].id;
    }
    this.updateBackendConfig();
  }

  onModelChange(): void {
    this.updateBackendConfig();
  }

  updateBackendConfig(): void {
    this.plannerService.updateConfig(this.selectedProvider, this.selectedModel).subscribe({
      next: (res) => console.log('Config updated:', res),
      error: (err) => console.error('Failed to update config:', err)
    });
  }

  sendMessage(): void {
    if (!this.userInput.trim()) return;

    const text = this.userInput;
    this.userInput = '';
    this.messages.push({ role: 'user', content: text });
    this.isLoading = true;
    this.scrollToBottom();

    if (!this.sessionId) {
      // Initial generation
      const request: ItineraryRequest = {
        description: text,
        provider: this.selectedProvider,
        model: this.selectedModel
      };

      this.plannerService.generateItinerary(request).subscribe({
        next: (response) => this.handleResponse(response),
        error: (err) => this.handleError(err)
      });
    } else {
      // Refinement
      const request: RefinementRequest = {
        session_id: this.sessionId,
        feedback: text
      };

      this.plannerService.refineItinerary(request).subscribe({
        next: (response) => this.handleResponse(response),
        error: (err) => this.handleError(err)
      });
    }
  }

  handleResponse(response: ItineraryResponse): void {
    console.log('Received response:', response);
    if (!response || !response.itinerary) {
      console.error('Invalid response received');
      this.handleError('Received empty response from server');
      return;
    }

    this.sessionId = response.session_id;
    this.messages.push({
      role: 'assistant',
      content: response.itinerary,
      followUpQuestions: response.follow_up_questions
    });
    this.isLoading = false;
    this.scrollToBottom();
  }

  handleError(err: any): void {
    console.error(err);
    this.messages.push({ role: 'assistant', content: 'Sorry, something went wrong. Please try again.' });
    this.isLoading = false;
    this.scrollToBottom();
  }

  useTemplate(template: any): void {
    this.userInput = template.desc; // Or title + desc
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      // Optional: Show a toast or change icon temporarily
      console.log('Copied to clipboard');
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  }

  scrollToBottom(): void {
    setTimeout(() => {
      if (this.scrollContainer) {
        this.scrollContainer.nativeElement.scrollTop = this.scrollContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
}
