<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Complaint;
use Illuminate\Http\Request;

class ComplaintController extends Controller
{
    public function index()
    {
        return response()->json(
            Complaint::query()->with('facility')->latest()->paginate(15)
        );
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'facility_id' => ['required', 'integer', 'exists:facilities,id'],
            'reported_by_user_id' => ['required', 'integer', 'exists:users,id'],
            'description' => ['required', 'string'],
            'status' => ['sometimes', 'string', 'in:open,in_progress,resolved'],
        ]);

        $complaint = Complaint::create($validated);

        return response()->json($complaint, 201);
    }

    public function show(Complaint $complaint)
    {
        return response()->json($complaint->load('facility'));
    }

    public function update(Request $request, Complaint $complaint)
    {
        $validated = $request->validate([
            'facility_id' => ['sometimes', 'required', 'integer', 'exists:facilities,id'],
            'reported_by_user_id' => ['sometimes', 'required', 'integer', 'exists:users,id'],
            'description' => ['sometimes', 'required', 'string'],
            'status' => ['sometimes', 'required', 'string', 'in:open,in_progress,resolved'],
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