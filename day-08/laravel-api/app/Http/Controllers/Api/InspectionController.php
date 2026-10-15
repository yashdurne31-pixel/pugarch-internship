<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\Inspection;
use Illuminate\\Http\\Request;

class InspectionController extends Controller
{
    public function index()
    {
        return response()->json(Inspection::query()->latest()->paginate(15));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'exists:facilities,id'],
            'inspector_user_id' => ['nullable', 'integer'],
            'inspection_date' => ['required', 'date'],
            'cleanliness_score' => ['required', 'integer', 'between:0,100'],
            'notes' => ['nullable', 'string']
        ]);
        return response()->json(Inspection::create($validated), 201);
    }

    public function show(Inspection $inspection)
    {
        return response()->json($inspection);
    }

    public function update(Request $request, Inspection $inspection)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'exists:facilities,id'],
            'inspector_user_id' => ['nullable', 'integer'],
            'inspection_date' => ['required', 'date'],
            'cleanliness_score' => ['required', 'integer', 'between:0,100'],
            'notes' => ['nullable', 'string']
        ]);
        $inspection->update($validated);
        return response()->json($inspection);
    }

    public function destroy(Inspection $inspection)
    {
        $inspection->delete();
        return response()->noContent();
    }
}
