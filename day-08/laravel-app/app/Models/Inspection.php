<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Inspection extends Model
{
    use HasFactory;

    public $timestamps = false;

    protected $fillable = [
        'facility_id',
        'inspector_user_id',
        'inspection_date',
        'cleanliness_score',
        'notes',
    ];

    protected function casts(): array
    {
        return [
            'inspection_date' => 'date',
            'cleanliness_score' => 'integer',
        ];
    }

    public function facility(): BelongsTo
    {
        return $this->belongsTo(Facility::class);
    }
}