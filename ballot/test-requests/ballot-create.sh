curl -s -H "Content-Type: Application/json" --data-binary @test-requests/ballot-create-1.json -X POST https://${API_ENDPOINT}/ballots
curl -s -H "Content-Type: Application/json" --data-binary @test-requests/ballot-create-2.json -X POST https://${API_ENDPOINT}/ballots
