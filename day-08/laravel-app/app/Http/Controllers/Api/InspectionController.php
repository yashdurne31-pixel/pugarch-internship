<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Inspection;
use Illuminate\Http\Request;

class InspectionController extends Controller
{
    public function index()
    {
        return response()->json(
            Inspection::query()->with('facility')->latest('inspection_date')->paginate(15)
        );
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'integer', 'exists:facilities,id'],
            'inspector_user_id' => ['required', 'integer', 'exists:users,id'],
            'inspection_date' => ['required', 'date'],
            'cleanliness_score' => ['required', 'integer', 'between:0,100'],
            'notes' => ['nullable', 'string'],
        ]);

        $inspection = Inspection::create($validated);

        return response()->json($inspection, 201);
    }

    public function show(Inspection $inspection)
    {
        return response()->json($inspection->load('facility'));
    }

    public function update(Request $request, Inspection $inspection)
    {
        $validated = $request->validate([
            'facility_id' => ['sometimes', 'required', 'integer', 'exists:facilities,id'],
            'inspector_user_id' => ['sometimes', 'required', 'integer', 'exists:users,id'],
            'inspection_date' => ['sometimes', 'required', 'date'],
            'cleanliness_score' => ['sometimes', 'required', 'integer', 'between:0,100'],
            'notes' => ['nullable', 'string'],
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