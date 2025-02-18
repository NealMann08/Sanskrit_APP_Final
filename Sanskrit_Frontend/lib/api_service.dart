import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://127.0.0.1:5000";  // Your Flask backend URL

  // Fetch Fill-in-the-Blank Exercise
  static Future<Map<String, dynamic>> fetchFillInTheBlank() async {
    final response = await http.get(Uri.parse('$baseUrl/fill-in-the-blank'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load exercise");
    }
  }

  // Fetch Image Generation Exercise
  static Future<Map<String, dynamic>> fetchImageGeneration(String prompt) async {
    final response = await http.post(
      Uri.parse('$baseUrl/generate-image'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"prompt": prompt}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to generate image");
    }
  }

  // Fetch Writing Analysis
  static Future<Map<String, dynamic>> fetchWritingAnalysis(String text) async {
    final response = await http.post(
      Uri.parse('$baseUrl/writing-analysis'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"text": text}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to analyze writing");
    }
  }

  // Fetch Translation Exercise
  static Future<Map<String, dynamic>> fetchTranslationExercise() async {
    final response = await http.get(Uri.parse('$baseUrl/translate'));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load translation exercise");
    }
  }
}

