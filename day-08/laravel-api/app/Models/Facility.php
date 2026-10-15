<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\Relations\\HasMany;

class Facility extends Model
{
    protected $fillable = ['name', 'location', 'cleanliness_score', 'status'];

    public function inspections(): HasMany
    {
        return $this->hasMany(Inspection::class);
    }

    public function complaints(): HasMany
    {
        return $this->hasMany(Complaint::class);
    }
}
