import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService } from '../core/services/api.service';
import { Facility, Inspection } from '../core/models/models';
@Component({selector:'app-inspections',standalone:true,imports:[CommonModule,RouterLink],template:`
<div class="heading"><div><h1 class="page-title">Inspections</h1><p class="page-subtitle">Review inspection activity and recorded results.</p></div><a class="btn primary" routerLink="/inspections/new">+ New inspection</a></div>
<div class="card"><div *ngIf="loading" class="notice">Loading inspections…</div><div *ngIf="error" class="error">{{error}}</div><p *ngIf="!loading&&!error&&!items.length" class="muted">No inspections found. You can create the first record.</p><div class="table-wrap" *ngIf="items.length"><table><thead><tr><th>ID</th><th>Facility</th><th>Date</th><th>Rating</th><th>Status</th></tr></thead><tbody><tr *ngFor="let i of items"><td>#{{i.id}}</td><td>{{facilityName(i)}}</td><td>{{date(i)}}</td><td>{{i.rating??i.cleanliness_score??'—'}}</td><td>{{i.status||'recorded'}}</td></tr></tbody></table></div></div>`,
styles:[`.heading{display:flex;justify-content:space-between;gap:12px;margin-bottom:20px}.muted{color:#697586}@media(max-width:600px){.heading{flex-direction:column}}`]
})
export class InspectionsPage implements OnInit {
 private api=inject(ApiService);items:Inspection[]=[];facilities:Facility[]=[];loading=true;error='';
 ngOnInit():void{this.api.facilities().subscribe({next:r=>this.facilities=r.data??[],error:()=>undefined});this.api.inspections().subscribe({next:r=>{this.items=Array.isArray(r)?r:r.data??[];this.loading=false},error:()=>{this.error='Unable to load inspections. Check that /api/inspections exists in Laravel.';this.loading=false}})}
 facilityName(i:Inspection):string{const f=this.facilities.find(x=>x.id===i.facility_id);return i.facility?.name??i.facility?.facility_name??f?.name??f?.facility_name??`Facility #${i.facility_id??'—'}`}
 date(i:Inspection):string{const d=i.inspection_date??i.date;return d?new Date(d).toLocaleDateString():'—'}
}
