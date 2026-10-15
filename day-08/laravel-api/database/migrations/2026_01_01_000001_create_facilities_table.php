<?php

use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('facilities', function (Blueprint $table) {
            $table->id();
            $table->string('name', 160);
            $table->string('location', 180);
            $table->unsignedTinyInteger('cleanliness_score')->default(0);
            $table->enum('status', ['active', 'maintenance', 'closed'])->default('active');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('facilities'); }
};
