<?php

use Illuminate\Support\Facades\Route;
use App\Models\Crime;



Route::get('/', function () {
    return view('welcome');
});
use App\Http\Controllers\CrimeController;

Route::get('/api/crimes', [CrimeController::class, 'index']);
Route::get('/api/crimes/{id}', [CrimeController::class, 'show']);


Route::get('/crimes', function () {
    return Crime::latest()->limit(50)->get();
});

