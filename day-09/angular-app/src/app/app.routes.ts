import { Routes } from '@angular/router';
import { DashboardPage } from './pages/dashboard.page';
import { FacilitiesPage } from './pages/facilities.page';
import { FacilityDetailPage } from './pages/facility-detail.page';
import { InspectionsPage } from './pages/inspections.page';
import { InspectionFormPage } from './pages/inspection-form.page';
export const routes: Routes = [
 {path:'',component:DashboardPage},
 {path:'facilities',component:FacilitiesPage},
 {path:'facilities/:id',component:FacilityDetailPage},
 {path:'inspections',component:InspectionsPage},
 {path:'inspections/new',component:InspectionFormPage},
 {path:'**',redirectTo:''}
];
