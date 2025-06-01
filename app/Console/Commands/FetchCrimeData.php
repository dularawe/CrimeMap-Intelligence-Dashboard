<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use App\Models\Crime;

class FetchCrimeData extends Command
{
    protected $signature = 'fetch:crimes';
    protected $description = 'Fetch crime data from ML API';

    public function handle()
    {
        $response = Http::get('http://127.0.0.1:8000/get-latest-crimes');

        if ($response->successful()) {
            foreach ($response->json() as $crime) {
                Crime::updateOrCreate(
                    ['title' => $crime['title'], 'source_url' => $crime['source_url']],
                    [
                        'description' => $crime['description'],
                        'category' => $crime['category'],
                        'latitude' => $crime['latitude'],
                        'longitude' => $crime['longitude'],
                    ]
                );
            }

            $this->info("Crime data updated successfully.");
        } else {
            $this->error(" Failed to fetch crime data.");
        }
    }
}
