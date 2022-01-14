import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { TweetService } from 'src/app/services/tweet.service';
import { tweet } from 'src/app/tweets';

@Component({
  selector: 'app-tweet-list',
  templateUrl: './tweet-list.component.html',
  styleUrls: ['./tweet-list.component.scss']
})
export class TweetListComponent implements OnInit {

  public tweets: any;
  public documents: number = 0;
  public total: number = 0;
  public actual: number = 0;
  public next: number = 20;
  public collections: string = "";

  constructor(
    private tweetService: TweetService,
    private router: Router
    ) { }

  ngOnInit(): void {
    this.reloadData();    
    this.Count_Documents();
    this.consigueCollection();
    this.tweetService.changeReload.subscribe(()=>{
      this.reloadData();
      this.Count_Documents();
      this.consigueCollection();
    });
  }

  consigueCollection(){
    this.tweetService.getCollections().subscribe(response => {
      this.collections = response;
      //console.log(response);
    });
  }

  show(i: number){
    document.getElementById(i.toString())?.classList.toggle("hidden")
  }

  anterior(actual: number){
    var colleccion = (<HTMLSelectElement>document.getElementById("selecciona")).value;
    var min = (20*actual)-20;
    var max = min + 20;
    this.actual = this.actual - 1;
    this.tweetService.getTweetsList(colleccion,min, max).subscribe(response => {
      this.tweets = response;
      //console.log(this.tweets);
    });  
  }

  siguientes(actual: number){
    var colleccion = (<HTMLSelectElement>document.getElementById("selecciona")).value;
    var min = 20*actual;
    var max = min + 20;
    this.actual = (actual - this.actual) + this.actual;
    this.tweetService.getTweetsList(colleccion,min, max).subscribe(response => {
      this.tweets = response;
      //console.log(this.tweets);
    });  
  }


  reloadData(){
    var colleccion = (<HTMLSelectElement>document.getElementById("selecciona")).value;
    this.actual = 0;
    //console.log("Reload");
    this.tweetService.getTweetsList(colleccion,0, 20).subscribe(response => {
      this.tweets = response;
      //console.log(this.tweets);
    });    
  }

  Count_Documents(){
    this.tweetService.getdocumentscount().subscribe(response => {
      this.documents = response;
      this.total = Math.trunc(response/20);
    });
  }

}
