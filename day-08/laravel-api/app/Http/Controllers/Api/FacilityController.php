<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\Facility;
use Illuminate\\Http\\Request;

class FacilityController extends Controller
{
    public function index()
    {
        return response()->json(Facility::query()->latest()->paginate(15));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:160'],
            'location' => ['required', 'string', 'max:180'],
            'cleanliness_score' => ['required', 'integer', 'between:0,100'],
            'status' => ['required', 'in:active,maintenance,closed']
        ]);
        return response()->json(Facility::create($validated), 201);
    }

    public function show(Facility $facility)
    {
        return response()->json($facility);
    }

    public function update(Request $request, Facility $facility)
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:160'],
            'location' => ['required', 'string', 'max:180'],
            'cleanliness_score' => ['required', 'integer', 'between:0,100'],
            'status' => ['required', 'in:active,maintenance,closed']
        ]);
        $facility->update($validated);
        return response()->json($facility);
    }

    public function destroy(Facility $facility)
    {
        $facility->delete();
        return response()->noContent();
    }
}
