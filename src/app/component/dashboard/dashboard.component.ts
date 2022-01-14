import { Component, OnInit } from '@angular/core';
import { timer } from 'rxjs';
import { consultas } from 'src/app/consultas';
import { TweetService } from 'src/app/services/tweet.service';
import { ChartType } from 'chart.js';
import { SingleDataSet, Label} from 'ng2-charts';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  public tweets: any;
  public collections: any;
  public dates: any;
  private colleccion: string = "tweets";
  public docs: number = 0;
  public mostrt: any;
  public morert: any;
  public verificados: any;
  public hashtags: any;
  public mencionados: any;
  public urls: any;
  public idiomas: any;
  
  public pieChartLabels: Label[] = [];
  public pieChartData: SingleDataSet = [];
  public pieChartType: ChartType = 'pie';

  public pieLabelsrt: Label[] = [];
  public pieDatart: SingleDataSet = [];
  
  constructor(
    private tweetService: TweetService, 
  ) {   }

  ngOnInit(): void {
    this.consigueCollection();
      timer(500).subscribe(x => {
        this.reload();
      })
  }

  reload(){    
    this.consigueFechas();
    this.consigueDocumentos();
    this.consigueMostrt();
    this.consigueMorert();
    this.consigueVerificados();
    this.consigueHashtags();
    this.consigueMasMencionados();
    this.consiguRrls();
    this.consigueIdiomas();
  }

  consigueCollection(){
    this.tweetService.getCollections().subscribe(response => {
      this.collections = response;
      //console.log(response);
    });
  }

  consigueFechas(){
    this.tweetService.getdates().subscribe(response => {
      this.dates = response;   
      // console.log(this.dates);
         
    })
  }

  getselec(){
    this.colleccion = (<HTMLSelectElement>document.getElementById("selecciona")).value;
  }

  consigueDocumentos(){
    this.tweetService.getdocumentscountcollection(this.colleccion).subscribe( response => {
      // console.log(response);
      this.docs = response;
    })
  }

  consigueMostrt(){
    this.tweetService.getmostrt(this.colleccion).subscribe(response => {
      this.mostrt = response;
      //console.log(response);
      
    })
  }

  consigueMorert(){
    this.tweetService.get5morert(this.colleccion).subscribe(response => {
      this.morert = response;
      this.morert.forEach((item: any) =>{
        //console.log(item._id);
        this.pieLabelsrt.push(item.user_name)
        this.pieDatart.push(item.suma)
      });
    })
  }

  consigueHashtags(){
    this.tweetService.getHashtags(this.colleccion).subscribe(response => {
      this.hashtags = response;
      console.log("Hashtags: ", response);
      
    })
  }

  consigueVerificados(){
    this.tweetService.getVerificados(this.colleccion).subscribe(response => {
      this.verificados = response;
      // console.log(this.verificados);
      
    })
  }

  consigueMasMencionados(){
    this.tweetService.getMoreMencionados(this.colleccion).subscribe(response => {
      this.mencionados = response;
    })
  }

  consiguRrls(){
    this.tweetService.getUrl(this.colleccion).subscribe(response => {
      this.urls = response;
    })
  }

  consigueIdiomas(){
    this.pieChartLabels = [];
    this.pieChartData = [];
    this.tweetService.getIdiomas(this.colleccion).subscribe(response => {
      this.idiomas = response;
      //console.log("Idiomas: ",Object.keys(this.idiomas).length );
      this.idiomas.forEach((item: any) =>{
        //console.log(item._id);
        this.pieChartLabels.push(item._id)
        this.pieChartData.push(item.suma)
      });
      
    })
  }


  nuevaBusqueda(){
    this.getselec();
    this.reload();
  }

  toggleRT(){
    document.getElementById("LabelRT")?.classList.toggle("hidden");
    document.getElementById("CanvasRT")?.classList.toggle("hidden");
  }

  toggleLang(){
    document.getElementById("LabelLang")?.classList.toggle("hidden");
    document.getElementById("CanvasLang")?.classList.toggle("hidden");
  }
}
