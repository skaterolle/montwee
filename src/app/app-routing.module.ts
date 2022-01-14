import { ConsultasComponent } from './component/consultas/consultas.component';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TweetListComponent } from './component/tweet-list/tweet-list.component';
import { DashboardComponent } from './component/dashboard/dashboard.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  { path: 'tweetslist', component: TweetListComponent },
  { path: 'consultas', component: ConsultasComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: '**', redirectTo: 'dashboard' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }