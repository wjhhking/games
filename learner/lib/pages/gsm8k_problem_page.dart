import 'package:flutter/material.dart';

class Gsm8kProblemPage extends StatefulWidget {
  final List<dynamic> problems;
  final int startingIndex;

  const Gsm8kProblemPage({
    super.key,
    required this.problems,
    this.startingIndex = 0,
  });

  @override
  State<Gsm8kProblemPage> createState() => _Gsm8kProblemPageState();
}

class _Gsm8kProblemPageState extends State<Gsm8kProblemPage> {
  late int _currentIndex;
  bool _showAnswer = false;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.startingIndex;
  }

  void _nextProblem() {
    if (_currentIndex < widget.problems.length - 1) {
      setState(() {
        _currentIndex++;
        _showAnswer = false;
      });
    }
  }

  void _previousProblem() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
        _showAnswer = false;
      });
    }
  }

  void _jumpToProblem(int index) {
    setState(() {
      if (index >= 0 && index < widget.problems.length) {
        _currentIndex = index;
        _showAnswer = false;
      }
    });
  }

  void _showJumpToGrid(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext context) {
        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 5,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
          ),
          itemCount: widget.problems.length,
          itemBuilder: (context, index) {
            return ElevatedButton(
              onPressed: () {
                _jumpToProblem(index);
                Navigator.pop(context);
              },
              child: FittedBox(
                fit: BoxFit.scaleDown,
                child: Text('${index + 1}'),
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final problem = widget.problems[_currentIndex];
    final question = problem['question']?.toString() ?? 'No question available.';
    final answer = problem['answer']?.toString() ?? 'No answer available.';

    return Scaffold(
      appBar: AppBar(
        title: Text('Problem ${_currentIndex + 1} of ${widget.problems.length}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              question,
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            if (_showAnswer)
              Container(
                padding: const EdgeInsets.all(12.0),
                decoration: BoxDecoration(
                  color: Colors.green.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.green.withOpacity(0.5)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Answer:',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: Colors.green[800],
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      answer,
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: Colors.green[800],
                          ),
                    ),
                  ],
                ),
              ),
            const SizedBox(height: 24),
            Center(
              child: ElevatedButton(
                onPressed: () {
                  setState(() {
                    _showAnswer = !_showAnswer;
                  });
                },
                child: Text(_showAnswer ? 'Hide Answer' : 'Show Answer'),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            TextButton.icon(
              icon: const Icon(Icons.arrow_back),
              label: const Text('Previous'),
              onPressed: _currentIndex > 0 ? _previousProblem : null,
            ),
            TextButton(
              child: const Text('Jump To'),
              onPressed: () => _showJumpToGrid(context),
            ),
            TextButton.icon(
              icon: const Icon(Icons.arrow_forward),
              label: const Text('Next'),
              onPressed: _currentIndex < widget.problems.length - 1
                  ? _nextProblem
                  : null,
            ),
          ],
        ),
      ),
    );
  }
} 