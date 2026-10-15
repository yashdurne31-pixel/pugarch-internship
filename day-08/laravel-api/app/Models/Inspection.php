<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use Illuminate\\Database\\Eloquent\\Relations\\BelongsTo;

class Inspection extends Model
{
    protected $fillable = ['facility_id', 'inspector_user_id', 'inspection_date', 'cleanliness_score', 'notes'];

    protected $casts = ['inspection_date' => 'date'];

    public function facility(): BelongsTo
    {
        return $this->belongsTo(Facility::class);
    }
}
