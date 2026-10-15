<?php

namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Models\\Complaint;
use Illuminate\\Http\\Request;

class ComplaintController extends Controller
{
    public function index()
    {
        return response()->json(Complaint::query()->latest()->paginate(15));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'exists:facilities,id'],
            'reported_by_user_id' => ['nullable', 'integer'],
            'description' => ['required', 'string'],
            'status' => ['required', 'in:open,in_progress,resolved'],
            'resolved_at' => ['nullable', 'date']
        ]);
        return response()->json(Complaint::create($validated), 201);
    }

    public function show(Complaint $complaint)
    {
        return response()->json($complaint);
    }

    public function update(Request $request, Complaint $complaint)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'exists:facilities,id'],
            'reported_by_user_id' => ['nullable', 'integer'],
            'description' => ['required', 'string'],
            'status' => ['required', 'in:open,in_progress,resolved'],
            'resolved_at' => ['nullable', 'date']
        ]);
        $complaint->update($validated);
        return response()->json($complaint);
    }

    public function destroy(Complaint $complaint)
    {
        $complaint->delete();
        return response()->noContent();
    }
}
