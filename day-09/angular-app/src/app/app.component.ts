import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
@Component({
 selector:'app-root', standalone:true, imports:[RouterLink,RouterLinkActive,RouterOutlet],
 template:`
 <div class="shell"><aside><a class="brand" routerLink="/">◈ Facility<span>Ops</span></a><p>WORKSPACE</p>
 <a routerLink="/" [routerLinkActiveOptions]="{exact:true}" routerLinkActive="active">▦ Dashboard</a>
 <a routerLink="/facilities" routerLinkActive="active">⌂ Facilities</a><a routerLink="/inspections" routerLinkActive="active">✓ Inspections</a>
 <div class="profile">YD &nbsp; Workspace Admin</div></aside>
 <main><header>Facility Management <span>● API workspace</span></header><section><router-outlet /></section><footer>FacilityOps · Facility inspection workspace</footer></main></div>`,
 styles:[`
 .shell{min-height:100vh;display:grid;grid-template-columns:235px 1fr}aside{background:#172541;color:#dce5f6;padding:24px 16px;display:flex;flex-direction:column;gap:8px}.brand{font-size:20px;font-weight:800;color:#fff;padding:0 8px 24px}.brand span{color:#8da4ff}aside p{font-size:10px;letter-spacing:1px;color:#8190aa;padding-left:10px}aside>a:not(.brand){padding:12px;border-radius:8px;color:#b9c5da}aside>a.active,aside>a:hover{background:#2b3c61;color:white}.profile{margin-top:auto;padding:18px 4px 0;border-top:1px solid #33425e;font-size:12px}main{min-width:0;display:flex;flex-direction:column}header{height:64px;background:white;border-bottom:1px solid #e5eaf0;padding:23px 28px;color:#697586;font-size:13px}header span{float:right;color:#16845b}section{padding:28px;flex:1}footer{padding:15px 28px;background:white;border-top:1px solid #e5eaf0;color:#697586;font-size:11px}@media(max-width:700px){.shell{grid-template-columns:1fr}aside{padding:12px}aside p,.profile{display:none}aside>a:not(.brand){display:inline-block}section{padding:16px}header{padding:22px 16px}}`]
})
export class AppComponent {}
