import 'package:flutter/material.dart';
import '../api_service.dart';

class FillInTheBlankScreen extends StatefulWidget {
  const FillInTheBlankScreen({super.key});

  @override
  _FillInTheBlankScreenState createState() => _FillInTheBlankScreenState();
}

class _FillInTheBlankScreenState extends State<FillInTheBlankScreen> {
  String exercise = "";
  List<String> choices = [];
  String correctAnswer = "";
  String feedback = "";

  @override
  void initState() {
    super.initState();
    fetchExercise();
  }

  Future<void> fetchExercise() async {
    try {
      final data = await ApiService.fetchFillInTheBlank();
      setState(() {
        exercise = data['exercise'];
        choices = List<String>.from(data['choices']); // Convert JSON list to Dart list
        correctAnswer = data['correct_answer'];
        feedback = ""; // Reset feedback when fetching new question
      });
    } catch (e) {
      print("Error fetching exercise: $e");
    }
  }

  void checkAnswer(String selectedAnswer) {
    setState(() {
      feedback = selectedAnswer == correctAnswer
          ? "✅ Correct!"
          : "❌ Incorrect. The correct answer is: $correctAnswer";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Fill-in-the-Blank Exercise')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Exercise:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(exercise, style: TextStyle(fontSize: 16)),
            SizedBox(height: 20),
            Column(
              children: choices.map((choice) {
                return ElevatedButton(
                  onPressed: () => checkAnswer(choice),
                  child: Text(choice),
                );
              }).toList(),
            ),
            SizedBox(height: 20),
            Text(feedback, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: fetchExercise,
              child: Text('Next Question'),
            ),
          ],
        ),
      ),
    );
  }
}
