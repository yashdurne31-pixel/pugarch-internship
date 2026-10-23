import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../core/services/api.service';
import { Facility } from '../core/models/models';
@Component({selector:'app-inspection-form',standalone:true,imports:[CommonModule,ReactiveFormsModule,RouterLink],template:`
<a routerLink="/inspections">← Back to inspections</a><h1 class="page-title form-title">New inspection</h1><p class="page-subtitle">Record an inspection and its findings.</p>
<div *ngIf="loading" class="notice">Loading facilities…</div><div *ngIf="error" class="error">{{error}}</div>
<form *ngIf="!loading" class="card form" [formGroup]="form" (ngSubmit)="submit()">
<label class="field">Facility<select formControlName="facility_id"><option [ngValue]="null">Select facility</option><option *ngFor="let f of facilities" [ngValue]="f.id">{{f.name||f.facility_name||('Facility #'+f.id)}}</option></select><small *ngIf="form.controls.facility_id.touched&&form.controls.facility_id.invalid" class="validation">Select a facility.</small></label>
<div class="two"><label class="field">Inspection date<input type="date" formControlName="inspection_date"><small *ngIf="form.controls.inspection_date.touched&&form.controls.inspection_date.invalid" class="validation">Date is required.</small></label><label class="field">Cleanliness score (0–100)<input type="number" min="0" max="100" formControlName="cleanliness_score"><small *ngIf="form.controls.cleanliness_score.touched&&form.controls.cleanliness_score.invalid" class="validation">Enter a score between 0 and 100.</small></label></div>
<div class="two"><label class="field">Status<select formControlName="status"><option value="completed">Completed</option><option value="pending">Pending</option><option value="overdue">Overdue</option></select></label><label class="field">Inspector name<input formControlName="inspector_name" placeholder="Inspector name"><small *ngIf="form.controls.inspector_name.touched&&form.controls.inspector_name.invalid" class="validation">Inspector name is required.</small></label></div>
<label class="field">Notes<textarea rows="4" formControlName="notes" placeholder="Observations and recommended actions"></textarea></label><div class="actions"><button type="button" class="btn" (click)="cancel()">Cancel</button><button class="btn primary" type="submit" [disabled]="saving">{{saving?'Saving…':'Save inspection'}}</button></div></form>`,
styles:[`.form-title{margin-top:22px}.form{max-width:800px;display:grid;gap:18px}.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.validation{color:#bf3d4b}.actions{display:flex;justify-content:flex-end;gap:10px;border-top:1px solid #e5eaf0;padding-top:16px}@media(max-width:600px){.two{grid-template-columns:1fr}}`]
})
export class InspectionFormPage implements OnInit {
 private fb=inject(FormBuilder);private api=inject(ApiService);private router=inject(Router);facilities:Facility[]=[];loading=true;saving=false;error='';
 form=this.fb.group({facility_id:[null as number|null,Validators.required],inspection_date:[new Date().toISOString().slice(0,10),Validators.required],cleanliness_score:[80,[Validators.required,Validators.min(0),Validators.max(100)]],status:['completed',Validators.required],inspector_name:['',Validators.required],notes:['',[Validators.maxLength(1000)]]});
 ngOnInit():void{this.api.facilities().subscribe({next:r=>{this.facilities=r.data??[];this.loading=false},error:()=>{this.error='Could not load facilities.';this.loading=false}})}
 submit():void{this.error='';if(this.form.invalid){this.form.markAllAsTouched();return}this.saving=true;const v=this.form.getRawValue();this.api.createInspection({facility_id:Number(v.facility_id),inspection_date:v.inspection_date??undefined,cleanliness_score:Number(v.cleanliness_score),status:v.status??'completed',inspector_name:v.inspector_name??'',notes:v.notes??''}).subscribe({next:()=>{this.saving=false;void this.router.navigate(['/inspections'])},error:e=>{this.saving=false;this.error=e?.error?.message??'Could not save inspection. Confirm the Laravel API accepts this payload.'}})}
 cancel():void{void this.router.navigate(['/inspections'])}
}
