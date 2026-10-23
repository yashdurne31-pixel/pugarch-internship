import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService } from '../core/services/api.service';
import { Facility } from '../core/models/models';
@Component({selector:'app-facilities',standalone:true,imports:[CommonModule,FormsModule,RouterLink],template:`
<div class="heading"><div><h1 class="page-title">Facilities</h1><p class="page-subtitle">Browse locations, filter status and inspect facility details.</p></div><button class="btn" (click)="reload()">Refresh</button></div>
<div class="card"><div class="toolbar"><label class="field">Search<input [(ngModel)]="search" placeholder="Name or location"></label><label class="field">Status<select [(ngModel)]="statusFilter"><option value="all">All statuses</option><option value="active">Active</option><option value="maintenance">Maintenance</option><option value="inactive">Inactive</option></select></label><label class="field">Sort<select [(ngModel)]="sortBy"><option value="name">Name A–Z</option><option value="score">Cleanliness score</option><option value="status">Status</option></select></label></div>
<div *ngIf="loading" class="notice">Loading facilities…</div><div *ngIf="error" class="error">{{error}}</div><p class="muted" *ngIf="!loading">{{filtered.length}} facilities found</p>
<div class="table-wrap" *ngIf="!loading&&filtered.length"><table><thead><tr><th>Facility</th><th>Location</th><th>Cleanliness</th><th>Status</th><th></th></tr></thead><tbody><tr *ngFor="let f of filtered"><td><b>{{name(f)}}</b><small class="id">ID #{{f.id}}</small></td><td>{{f.location||f.city||'—'}}</td><td>{{f.cleanliness_score??'—'}}</td><td><span class="badge" [class.maintenance]="status(f)==='maintenance'" [class.inactive]="status(f)==='inactive'">{{status(f)}}</span></td><td><a [routerLink]="['/facilities',f.id]">Details →</a></td></tr></tbody></table></div><p *ngIf="!loading&&!error&&!filtered.length" class="muted">No matching facilities.</p></div>`,
styles:[`.heading{display:flex;justify-content:space-between;gap:12px;margin-bottom:20px}.toolbar{display:flex;gap:12px;flex-wrap:wrap}.toolbar>*{flex:1 1 170px}.id{display:block;font-size:11px;color:#697586;margin-top:4px}.muted{color:#697586;font-size:12px}@media(max-width:600px){.heading{flex-direction:column}}`]
})
export class FacilitiesPage implements OnInit {
 private api=inject(ApiService);facilities:Facility[]=[];loading=true;error='';search='';statusFilter='all';sortBy='name';
 ngOnInit():void{this.reload()}
 get filtered():Facility[]{const term=this.search.trim().toLowerCase();return this.facilities.filter(f=>(!term||`${this.name(f)} ${f.location??''} ${f.city??''}`.toLowerCase().includes(term))&&(this.statusFilter==='all'||this.status(f)===this.statusFilter)).sort((a,b)=>this.sortBy==='score'?Number(b.cleanliness_score??0)-Number(a.cleanliness_score??0):this.sortBy==='status'?this.status(a).localeCompare(this.status(b)):this.name(a).localeCompare(this.name(b)))}
 name(f:Facility):string{return String(f.name??f.facility_name??`Facility #${f.id}`)}
 status(f:Facility):string{return String(f.operational_status??f.status??'unknown').toLowerCase()}
 reload():void{this.loading=true;this.error='';this.api.facilities().subscribe({next:r=>{this.facilities=r.data??[];this.loading=false},error:()=>{this.error='Could not load facilities. Ensure Laravel is running on port 8000.';this.loading=false}})}
}
