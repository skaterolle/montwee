import { TweetService } from 'src/app/services/tweet.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-consultas',
  templateUrl: './consultas.component.html',
  styleUrls: ['./consultas.component.scss']
})
export class ConsultasComponent implements OnInit {

  public ordena: string = "ASC";
  public tweets: any;
  public collections: any;

  constructor(
    private tweetService: TweetService,
  ) { }

  ngOnInit(): void {
    this.consigueCollection();
    this.tweetService.changeReload.subscribe(()=>{
      this.consigueCollection();
      this.tweets = [];
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
    console.log(i);
    
  }

  Guardar_Colleccion(){
    var nueva = (<HTMLInputElement>document.getElementById("nueva")).value;
    this.tweetService.Guarda_colleccion(this.tweets, nueva).subscribe(response => {
      console.log(response);
      
    });
  }

  find(){
    var colleccion = (<HTMLSelectElement>document.getElementById("selecciona")).value;
    var text = <HTMLInputElement>document.getElementById("texto");
    var orden: number = 1;
    var texto: string = "";
    var descartar_rt: boolean = false;
    var desde: any = "False";
    var hasta: any = "False";
    var usuario: string = "";
    var hashtag: string = "";
    var busca_hashtag: boolean = false;
    var menciones: number = 0;
    var geo: boolean = false;
    var verificado: boolean = false;

    if(this.ordena == "ASC"){
      orden = 1;
    }else if(this.ordena == "DES"){
      orden = -1;
    }
    if(text.value != ""){
      texto = text.value;
    }
    if((<HTMLInputElement>document.getElementById("descartar")).checked){
      descartar_rt = true;
    }else if (!(<HTMLInputElement>document.getElementById("descartar")).checked){
      descartar_rt = false;
    }    

    if((<HTMLInputElement>document.getElementById("desde")).value != ""){
      desde = new Date((<HTMLInputElement>document.getElementById("desde")).value);
      //console.log(desde);
    }

    if((<HTMLInputElement>document.getElementById("hasta")).value != ""){
      hasta = new Date((<HTMLInputElement>document.getElementById("hasta")).value);
      //console.log(hasta);
    }

    if((<HTMLInputElement>document.getElementById("user")).value != ""){
      usuario = (<HTMLInputElement>document.getElementById("user")).value;
      //console.log(user);
    }

    if((<HTMLInputElement>document.getElementById("hashtag")).value != ""){
      hashtag = (<HTMLInputElement>document.getElementById("hashtag")).value;
      if((<HTMLInputElement>document.getElementById("busca_hashtag")).checked){
        busca_hashtag = true;
      }else if (!(<HTMLInputElement>document.getElementById("busca_hashtag")).checked){
        busca_hashtag = false;
      } 
      //console.log(user);
    }

    // if((<HTMLInputElement>document.getElementById("menciones")).value != ""){
    //   menciones = parseInt((<HTMLInputElement>document.getElementById("menciones")).value);
    //   //console.log(user);
    // }

    if((<HTMLInputElement>document.getElementById("geo")).checked){
      geo = true;
    }else if (!(<HTMLInputElement>document.getElementById("geo")).checked){
      geo = false;
    } 

    if((<HTMLInputElement>document.getElementById("verificado")).checked){
      verificado = true;
    }else if (!(<HTMLInputElement>document.getElementById("verificado")).checked){
      verificado = false;
    } 
    

    this.tweetService.find(colleccion ,texto, orden, descartar_rt, desde, hasta, usuario, hashtag, busca_hashtag, menciones, geo, verificado).subscribe(responde => {
      this.tweets = responde;
      console.log(this.tweets);
    })

  }


  change(){
    if(this.ordena == "ASC"){
      this.ordena = "DES";
    }else{
      this.ordena = "ASC"
    }
  }

}
