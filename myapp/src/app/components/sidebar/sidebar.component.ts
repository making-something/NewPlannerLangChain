import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {
  folders = [
    { name: 'Work chats', color: 'border-l-green-400' },
    { name: 'Life chats', color: 'border-l-purple-400' },
    { name: 'Projects chats', color: 'border-l-yellow-400' },
    { name: 'Clients chats', color: 'border-l-blue-400' }
  ];

  chats = [
    { title: 'Plan a 3-day trip', preview: 'A 3-day trip to see the northern lights in Norway...' },
    { title: 'Ideas for a customer loyalty program', preview: 'Here are seven ideas for a customer loyalty...' },
    { title: 'Help me pick', preview: 'Here are some gift ideas for your fishing-loving...' }
  ];
}
