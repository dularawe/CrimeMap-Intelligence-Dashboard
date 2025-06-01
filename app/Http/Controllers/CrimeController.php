<?php



namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Crime;

class CrimeController extends Controller
{
    // GET /api/crimes
    public function index()
    {
        return response()->json(Crime::latest()->limit(50)->get());
    }

    // Optional: GET /api/crimes/{id}
    public function show($id)
    {
        return response()->json(Crime::findOrFail($id));
    }
}
