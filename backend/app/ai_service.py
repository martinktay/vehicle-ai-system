"""
AI Insight Service (Optional)

Architecture: Cloud extension layer
Purpose: Provide AI-powered fuel recommendations using OpenAI

This service is an OPTIONAL cloud extension. The core system works
without it. If OPENAI_API_KEY is not set, a graceful fallback is returned.

Design: Does NOT override ESP32 edge decisions. Provides advisory insights only.
"""

import os
from app.schemas import AIInsightRequest, AIInsightResponse

# Check for OpenAI availability
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai_client = None

if OPENAI_API_KEY and OPENAI_API_KEY != "sk-your-key-here":
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("[OK] OpenAI client initialized for AI insights")
    except ImportError:
        print("[WARN] openai package not installed - AI insights will use fallback")
    except Exception as e:
        print(f"[ERROR] OpenAI initialization failed: {e} - using fallback")
else:
    print("[INFO] OPENAI_API_KEY not set - AI insights will use fallback")


def generate_fallback_insight(data: AIInsightRequest) -> AIInsightResponse:
    """
    Generate a rule-based fallback insight when OpenAI is unavailable.
    
    This provides useful advice without requiring an API key.
    """
    # Determine risk level
    if data.status == "HIGH TEMP":
        risk = "HIGH"
        rec = "Reduce engine load and activate cooling. Consider switching to CNG for lower heat output."
        roadworthy = "Vehicle should be inspected — high temperature may indicate cooling system issues."
        climate = "High temperatures increase emissions. Switching to LPG/CNG reduces CO2 by 15-25%."
        operator = "⚠️ Engine running hot. Reduce speed and check coolant level."
        confidence = "HIGH"
    elif data.status == "LOW FUEL":
        risk = "MODERATE"
        rec = "Switch to CNG if available. Plan refueling stop within 10km."
        roadworthy = "Vehicle is roadworthy but fuel reserves are critically low."
        climate = "Low fuel operation is inefficient. Refuel soon to maintain optimal combustion."
        operator = "⛽ Fuel level critical. Switch to CNG and locate nearest fuel station."
        confidence = "HIGH"
    elif data.fuel_mode == "CNG":
        risk = "LOW"
        rec = "Continue on CNG — excellent efficiency and lowest emissions option."
        roadworthy = "Vehicle operating normally on CNG."
        climate = "CNG produces 25% less CO2 than petrol. Excellent environmental choice."
        operator = "✅ Running efficiently on CNG. All systems normal."
        confidence = "HIGH"
    elif data.fuel_mode == "LPG":
        risk = "LOW"
        rec = "LPG mode is efficient. Monitor temperature and consider CNG if available."
        roadworthy = "Vehicle operating normally on LPG."
        climate = "LPG produces 15% less CO2 than petrol. Good environmental choice."
        operator = "✅ Running on LPG. Good efficiency."
        confidence = "MEDIUM"
    else:
        risk = "LOW"
        rec = "Normal operation on petrol. Consider switching to LPG/CNG for cost savings."
        roadworthy = "Vehicle is fully roadworthy."
        climate = "Petrol mode has baseline emissions. LPG/CNG would reduce CO2 by 15-25%."
        operator = "✅ All systems normal. Consider LPG/CNG for better efficiency."
        confidence = "MEDIUM"

    return AIInsightResponse(
        recommendation=rec,
        confidence=confidence,
        risk_level=risk,
        roadworthiness=roadworthy,
        climate_note=climate,
        operator_message=operator,
        source="fallback"
    )


async def generate_ai_insight(data: AIInsightRequest) -> AIInsightResponse:
    """
    Generate AI-powered insight using OpenAI (if available).
    Falls back to rule-based logic if OpenAI is unavailable.
    """
    if openai_client is None:
        return generate_fallback_insight(data)

    try:
        prompt = f"""You are an AI vehicle advisor for a multi-fuel vehicle optimization system in Nigeria.

Current telemetry:
- Vehicle: {data.vehicle_id}
- Temperature: {data.temperature}°C
- Fuel Level: {data.fuel_percent}%
- Current Fuel Mode: {data.fuel_mode}
- System Status: {data.status}
- Relay 1 (Cooling): {data.relay1}
- Relay 2 (Fuel Switch): {data.relay2}
- Light Level (LDR): {data.ldr}
- Thermistor: {data.thermistor}
- Current Decision: {data.reason}

Respond with a JSON object containing exactly these fields:
- recommendation: One sentence fuel/driving recommendation
- confidence: HIGH, MEDIUM, or LOW
- risk_level: LOW, MODERATE, HIGH, or CRITICAL
- roadworthiness: One sentence about vehicle condition
- climate_note: One sentence about environmental impact
- operator_message: Short message for the driver (use emoji)

Consider Nigerian context: fuel prices, Lagos traffic, Harmattan season, CNG/LPG availability."""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a vehicle AI advisor. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        import json
        content = response.choices[0].message.content.strip()
        
        # Try to parse the JSON response
        if content.startswith("```"):
            # Strip markdown code block
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        result = json.loads(content)

        return AIInsightResponse(
            recommendation=result.get("recommendation", "No recommendation available"),
            confidence=result.get("confidence", "MEDIUM"),
            risk_level=result.get("risk_level", "LOW"),
            roadworthiness=result.get("roadworthiness", "Unable to assess"),
            climate_note=result.get("climate_note", "No climate data"),
            operator_message=result.get("operator_message", "Check vehicle status"),
            source="ai"
        )

    except Exception as e:
        print(f"[AI] OpenAI request failed: {e} - using fallback")
        return generate_fallback_insight(data)
