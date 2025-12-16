import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlannerService } from '../../services/planner.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {
  
  constructor(private plannerService: PlannerService) {}

  chats = [
    { title: 'Plan a 3-day trip', preview: 'A 3-day trip to see the northern lights in Norway...' },
    { title: 'Help me find the best place for me ', preview: 'what are best places for a ...' },
    { title: 'Help me pick', preview: 'Here are some ideas for ...' }
  ];

  startNewChat(): void {
    this.plannerService.triggerResetChat();
  }
}
