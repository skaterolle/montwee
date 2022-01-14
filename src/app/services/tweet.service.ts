import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TweetService {

  //En caso de 
  private online = 'http://129.151.230.102:5000';
  private local = 'http://192.168.1.139:5000';

  private baseUrl = '0'
  //private baseUrl = 'http://192.168.1.139:5000'
  //private baseUrl = 'http://129.151.230.102:5000'
  private reload = new Subject();
  public changeReload = this.reload.asObservable();


  constructor(private http: HttpClient) { 
    if(localStorage.URL){
      if(localStorage.URL != "true"){
        this.baseUrl = "http://"+ localStorage.URL +":5000";
      }else{
        this.baseUrl = this.local;
      }
    }else{
      this.baseUrl = this.online;
    }
    //console.log(localStorage.URL);
    //console.log(this.baseUrl);
  }


  setURL( estado: boolean, url: string){
    if(estado == true){
      if(url != ""){
        this.baseUrl = "http://"+url+":5000";
      }else{
        this.baseUrl = this.local
      }
    }else{
      this.baseUrl = this.online;
    }
    this.reload.next();
  }

  getTweetsList(colleccion: string ,min: number, max: number): Observable<any>{
    
    const data = ({'min':min, 'max':max, 'colleccion': colleccion});
    return this.http.post(`${this.baseUrl}/tweets`, data);
  }

  Guarda_colleccion(tweet: any, colleccion: string): Observable<any>{
    const data = ({
      'colleccion': tweet, 
      'nombre': colleccion
    }); 
    const resultado = this.http.post(`${this.baseUrl}/guarda`, data);
    this.reload.next();
    return resultado;
  }

  find(colleccion: string,text: string, order: number, descartar_rt: boolean, desde: any, hasta: any, usuario: string, hashtag: string, busca_hashtag: boolean, menciones: number, geo: boolean, verificado: boolean): Observable<any>{
    const data = ({
      'text': text, 
      'order': order, 
      'descart_rt': descartar_rt, 
      'desde': desde, 
      'hasta': hasta, 
      'usuario': usuario, 
      'hashtag': hashtag, 
      'busca_hashtag': busca_hashtag, 
      'menciones': menciones, 
      'geo': geo,
      'verificado': verificado,
      'colleccion': colleccion  
    });
    return this.http.post(`${this.baseUrl}/find`, data);
  }

  getdocumentscount(): Observable<any>{
    return this.http.get(`${this.baseUrl}/counts`)
  }

  getdocumentscountcollection(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/counts`, data)
  }

  getmostrt(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/mostrt`, data)
  }

  get5morert(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/5morert`, data)
  }

  getVerificados(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/verificados`, data)
  }

  getHashtags(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/hashtags`, data)
  }

  getMoreMencionados(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/5moremecionados`, data)
  }

  getUrl(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/5urls`, data)
  }

  getIdiomas(nombre: string): Observable<any>{
    const data = ({
      'nombre': nombre,
    });
    return this.http.post(`${this.baseUrl}/5idiomas`, data)
  }

  getdates(): Observable<any>{
    return this.http.get(`${this.baseUrl}/firstlast`)
  }

  getCollections(): Observable<any>{
    return this.http.get(`${this.baseUrl}/collections`)
  }

}
