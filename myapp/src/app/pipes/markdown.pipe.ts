import { Pipe, PipeTransform } from '@angular/core';
import { marked } from 'marked';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'markdown',
  standalone: true
})
export class MarkdownPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    if (!value) {
      return '';
    }

    // Unescape markdown links if they were escaped by the LLM
    // Some LLMs might escape brackets like \[Text\](Url)
    let cleanValue = value.replace(/\\\[/g, '[').replace(/\\\]/g, ']');

    let html = marked.parse(cleanValue) as string;
    
    // Simple regex replacement to add target="_blank" to links
    html = html.replace(/<a /g, '<a target="_blank" rel="noopener noreferrer" ');

    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}
