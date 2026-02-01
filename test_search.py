#!/usr/bin/env python3
"""
Test script for CloudJobHunt search functionality
"""
import sys
import requests
from datetime import datetime

# Configuration
BASE_URL = "https://api.cloudjobhunt.tn"
LOCAL_URL = "http://localhost:8000"

def test_search(query, location="", job_type=""):
    """Test the search endpoint"""
    url = f"{BASE_URL}/api/v1/search"
    params = {
        "q": query,
        "location": location,
        "job_type": job_type,
        "max_results": 10
    }
    
    print(f"\n{'='*60}")
    print(f"🔍 Test: Recherche '{query}' à '{location or 'France'}'")
    print(f"{'='*60}")
    
    try:
        print(f"📡 URL: {url}")
        print(f"📋 Params: {params}")
        response = requests.get(url, params=params, timeout=30)
        
        print(f"\n📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Succès!")
            print(f"   - Total trouvé: {data.get('total_found', 0)}")
            print(f"   - Jobs: {len(data.get('jobs', []))}")
            print(f"   - Timestamp: {data.get('searched_at', 'N/A')}")
            
            jobs = data.get('jobs', [])
            if jobs:
                print(f"\n📋 Exemples d'offres:")
                for i, job in enumerate(jobs[:5], 1):
                    print(f"\n   {i}. {job.get('title', 'N/A')}")
                    print(f"      🏢 Entreprise: {job.get('company', 'N/A')}")
                    print(f"      📍 Lieu: {job.get('location', 'N/A')}")
                    print(f"      💰 Salaire: {job.get('salary', 'N/A')}")
                    print(f"      📋 Type: {job.get('job_type', 'N/A')}")
                    print(f"      🏷️  Compétences: {', '.join(job.get('skills', []))}")
                    print(f"      🔗 Source: {job.get('source', 'N/A')}")
            return True
        else:
            print(f"\n❌ Erreur: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ Erreur de connexion: {e}")
        print(f"\n💡 Conseil: Assurez-vous que le serveur est en cours d'exécution.")
        print(f"   Pour tester localement: python main.py")
        return False
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return False

def test_health():
    """Test health endpoint"""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_public():
    """Test public endpoint"""
    url = f"{BASE_URL}/api/v1/test-public"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Test public: {data.get('message')}")
            return True
        else:
            print(f"❌ Test public: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test public error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 CloudJobHunt - Test de recherche")
    print("="*60)
    
    # Test health first
    print("\n1. Test Health Check...")
    health_ok = test_health()
    
    # Test public endpoint
    print("\n2. Test Endpoint Public...")
    public_ok = test_public()
    
    # Test search queries
    test_queries = [
        ("junior devops engineer", "Paris", ""),
        ("python developer", "France", "cdi"),
        ("data scientist", "Berlin", ""),
        ("stage", "Lyon", "stage"),
    ]
    
    print("\n3. Tests de recherche...")
    results = []
    for query, location, job_type in test_queries:
        ok = test_search(query, location, job_type)
        results.append((query, ok))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Résumé des tests")
    print("="*60)
    print(f"Health: {'✅ OK' if health_ok else '❌ FAIL'}")
    print(f"Public: {'✅ OK' if public_ok else '❌ FAIL'}")
    for query, ok in results:
        print(f"Search '{query}': {'✅ OK' if ok else '❌ FAIL'}")
    
    # Exit with appropriate code
    all_ok = health_ok and public_ok and all(ok for _, ok in results)
    sys.exit(0 if all_ok else 1)
