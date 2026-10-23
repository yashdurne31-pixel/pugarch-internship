import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ApiService } from '../core/services/api.service';
import { Facility, Inspection, Paginated } from '../core/models/models';
@Component({selector:'app-dashboard',standalone:true,imports:[CommonModule,RouterLink],template:`
<div class="heading"><div><h1 class="page-title">Dashboard overview</h1><p class="page-subtitle">Monitor facility health and inspection activity.</p></div><a class="btn primary" routerLink="/inspections/new">+ New inspection</a></div>
<div *ngIf="loading" class="notice">Loading dashboard…</div><div *ngIf="error" class="error">{{error}}</div>
<div class="stats"><article class="card"><span>Total facilities</span><strong>{{facilities.length}}</strong><small>Registered locations</small></article><article class="card"><span>Active facilities</span><strong>{{activeFacilities}}</strong><small>Operational locations</small></article><article class="card"><span>Maintenance</span><strong>{{maintenanceFacilities}}</strong><small>Need attention</small></article><article class="card"><span>Avg. cleanliness</span><strong>{{averageRating}}<small> / 100</small></strong><small>Loaded facilities</small></article></div>
<div class="grid"><section class="card"><h2>Recent inspections</h2><div class="table-wrap"><table><thead><tr><th>Facility</th><th>Rating</th><th>Date</th></tr></thead><tbody><tr *ngFor="let item of recentInspections"><td>{{inspectionFacility(item)}}</td><td>{{rating(item)}}</td><td>{{date(item)}}</td></tr></tbody></table></div><p *ngIf="!loading&&!recentInspections.length" class="muted">No inspection records found.</p><a routerLink="/inspections">View inspections →</a></section>
<section class="card"><h2>Facilities</h2><a class="row" *ngFor="let f of facilities.slice(0,5)" [routerLink]="['/facilities',f.id]"><span><b>{{name(f)}}</b><small>{{f.location||f.city||'Location not set'}}</small></span><span class="badge" [class.maintenance]="status(f)==='maintenance'">{{status(f)}}</span></a><a routerLink="/facilities">View all facilities →</a></section></div>`,
styles:[`.heading{display:flex;justify-content:space-between;align-items:start;gap:14px;margin-bottom:20px}.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:18px}.stats article{display:grid;gap:10px}.stats article>span,.stats small{font-size:12px;color:#697586}.stats strong{font-size:30px}.grid{display:grid;grid-template-columns:1.3fr 1fr;gap:16px}.grid h2{font-size:17px;margin-top:0}.row{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:13px 0;border-bottom:1px solid #e5eaf0;color:#172b4d}.row small{display:block;color:#697586;margin-top:5px;font-size:11px}.muted{color:#697586}@media(max-width:950px){.stats{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}}@media(max-width:550px){.heading{flex-direction:column}}`]
})
export class DashboardPage implements OnInit {
 private api=inject(ApiService); facilities:Facility[]=[]; inspections:Inspection[]=[]; loading=true; error='';
 ngOnInit():void{forkJoin({f:this.api.facilities().pipe(catchError(()=>of({data:[],current_page:1,last_page:1,total:0} as Paginated<Facility>))),i:this.api.inspections().pipe(catchError(()=>of([] as Inspection[])))}).subscribe({next:r=>{this.facilities=r.f.data??[];this.inspections=Array.isArray(r.i)?r.i:r.i.data??[];this.loading=false;},error:()=>{this.error='Unable to load dashboard data.';this.loading=false;}});}
 get activeFacilities():number{return this.facilities.filter(f=>this.status(f)==='active').length}
 get maintenanceFacilities():number{return this.facilities.filter(f=>this.status(f)==='maintenance').length}
 get averageRating():number{const scores=this.facilities.map(f=>Number(f.cleanliness_score)).filter(n=>Number.isFinite(n));return scores.length?Math.round(scores.reduce((a,b)=>a+b,0)/scores.length):0}
 get recentInspections():Inspection[]{return [...this.inspections].sort((a,b)=>this.time(b)-this.time(a)).slice(0,5)}
 name(f:Facility):string{return String(f.name??f.facility_name??`Facility #${f.id}`)}
 status(f:Facility):string{return String(f.operational_status??f.status??'unknown').toLowerCase()}
 inspectionFacility(i:Inspection):string{return i.facility?.name??i.facility?.facility_name??this.name(this.facilities.find(f=>f.id===i.facility_id)??{id:i.facility_id??0})}
 rating(i:Inspection):string{return String(i.rating??i.cleanliness_score??'—')}
 date(i:Inspection):string{const d=i.inspection_date??i.date;return d?new Date(d).toLocaleDateString():'—'}
 private time(i:Inspection):number{return new Date(i.inspection_date??i.date??0).getTime()||0}
}
