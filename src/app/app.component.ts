import { TweetService } from 'src/app/services/tweet.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'montwee';
  count: number = 0;
  estado: string = "local";

  constructor(
    private router: Router,
    private tweetService: TweetService
  ) {
  }
  
  ngOnInit(): void {
    this.Count_Documents();   
    this.comprueba();    
    if(localStorage.URL && localStorage.URL != "true"){
      (<HTMLInputElement>document.getElementById("url")).value = localStorage.URL;
    }
  }

  comprueba(){
    if(!localStorage.URL){
      document.getElementById("online")?.removeAttribute("checked");
      this.estado = "online";
    }else{
      this.estado = "local";
    }
  }

  Count_Documents(){
    this.count = 0;
    this.tweetService.getdocumentscount().subscribe(response => {
      this.count = response;
      //console.log("Total de documentos: ", this.count);
      
    });
  }

  cambio(){
    var checkbox = <HTMLInputElement>  document.getElementById("online");
    if(checkbox.checked){
      this.change();
    }
  }

  change(){
    var checkbox = <HTMLInputElement>  document.getElementById("online");
    if(checkbox.checked){
      var url =<HTMLInputElement>document.getElementById("url");
      if(url.value != ""){
        this.tweetService.setURL(true, url.value);
        localStorage.setItem("URL", url.value);
      }else{
        this.tweetService.setURL(true, url.value);
        localStorage.setItem("URL", "true");
      }
      this.estado = "local"
    }else{
      this.tweetService.setURL(false, "");
      localStorage.removeItem("URL");
      this.estado = "online";
    }
    this.Count_Documents();
  }
}
