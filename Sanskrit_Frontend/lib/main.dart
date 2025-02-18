import 'package:flutter/material.dart';

// Import your exercise screens here
import 'writing_analysis.dart';
import 'translation.dart';
import 'img_gen.dart';
import 'fill_in_the_blank.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sanskrit Learning App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Sanskrit Learning App'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // Method to handle navigation to any screen
  void navigateToScreen(Widget screen) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => screen),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.blue),
              child: Text(
                'Select an Exercise',
                style: TextStyle(color: Colors.white, fontSize: 24),
              ),
            ),
            // List of exercises with navigation
            _createDrawerItem('Writing Analysis', WritingAnalysisScreen()),
            _createDrawerItem('Translation', TranslationScreen()),
            _createDrawerItem('Image Generation', ImageGenerationScreen()),
            _createDrawerItem('Fill-in-the-Blank', FillInTheBlankScreen()),
          ],
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Welcome to Sanskrit Learning!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to the Writing Analysis screen
                navigateToScreen(WritingAnalysisScreen());
              },
              child: Text("Start Learning"),
            ),
          ],
        ),
      ),
    );
  }

  // Helper method to reduce code duplication for drawer items
  ListTile _createDrawerItem(String title, Widget screen) {
    return ListTile(
      title: Text(title),
      onTap: () {
        // Close the drawer and navigate to the selected screen
        Navigator.pop(context); // Close the drawer before navigating
        navigateToScreen(screen);
      },
    );
  }
}
