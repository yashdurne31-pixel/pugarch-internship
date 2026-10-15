<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('inspections', function (Blueprint $table) {
            $table->id();
            $table->foreignId('facility_id')->constrained()->cascadeOnDelete();
            $table->unsignedBigInteger('inspector_user_id')->nullable();
            $table->date('inspection_date');
            $table->unsignedTinyInteger('cleanliness_score');
            $table->text('notes')->nullable();
            $table->timestamps();
            $table->index(['facility_id', 'inspection_date']);
        });
    }
    public function down(): void { Schema::dropIfExists('inspections'); }
};
