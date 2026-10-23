import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ApiService } from '../core/services/api.service';
import { Facility, Inspection } from '../core/models/models';
@Component({selector:'app-facility-detail',standalone:true,imports:[CommonModule,RouterLink],template:`
<a routerLink="/facilities">← Back to facilities</a><div *ngIf="loading" class="notice">Loading facility…</div><div *ngIf="error" class="error">{{error}}</div>
<ng-container *ngIf="facility as f"><h1 class="page-title detail-title">{{name(f)}}</h1><p class="page-subtitle">{{f.location||f.city||'Location not set'}} · Facility #{{f.id}}</p><div class="stats"><article class="card"><span>Cleanliness score</span><strong>{{f.cleanliness_score??'—'}}<small> / 100</small></strong></article><article class="card"><span>Inspection records</span><strong>{{inspections.length}}</strong></article><article class="card"><span>Status</span><strong>{{f.operational_status||f.status||'unknown'}}</strong></article></div><div class="card"><h2>Inspection history</h2><p *ngIf="!inspections.length" class="muted">No inspection history available.</p><div class="table-wrap" *ngIf="inspections.length"><table><thead><tr><th>Date</th><th>Rating</th><th>Status</th><th>Notes</th></tr></thead><tbody><tr *ngFor="let i of inspections"><td>{{date(i)}}</td><td>{{i.rating??i.cleanliness_score??'—'}}</td><td>{{i.status||'recorded'}}</td><td>{{i.notes||'—'}}</td></tr></tbody></table></div></div></ng-container>`,
styles:[`.detail-title{margin-top:22px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0}.stats article{display:grid;gap:12px}.stats article span,.stats small,.muted{color:#697586}.stats strong{font-size:24px}@media(max-width:600px){.stats{grid-template-columns:1fr}}`]
})
export class FacilityDetailPage implements OnInit {
 private api=inject(ApiService);private route=inject(ActivatedRoute);facility:Facility|null=null;inspections:Inspection[]=[];loading=true;error='';
 ngOnInit():void{const id=Number(this.route.snapshot.paramMap.get('id'));if(!id){this.error='Invalid facility ID';this.loading=false;return}forkJoin({f:this.api.facility(id),i:this.api.inspections(id).pipe(catchError(()=>of([] as Inspection[])))}).subscribe({next:r=>{this.facility=r.f;this.inspections=Array.isArray(r.i)?r.i:r.i.data??[];this.loading=false},error:()=>{this.error='Unable to load facility details';this.loading=false}})}
 name(f:Facility):string{return String(f.name??f.facility_name??`Facility #${f.id}`)}
 date(i:Inspection):string{const d=i.inspection_date??i.date;return d?new Date(d).toLocaleDateString():'—'}
}
