<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\Relations\\BelongsTo;

class Complaint extends Model
{
    protected $fillable = ['facility_id', 'reported_by_user_id', 'description', 'status', 'resolved_at'];

    protected $casts = ['resolved_at' => 'datetime'];

    public function facility(): BelongsTo
    {
        return $this->belongsTo(Facility::class);
    }
}
