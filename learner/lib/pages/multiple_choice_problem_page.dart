import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class MultipleChoiceProblemPage extends StatefulWidget {
  const MultipleChoiceProblemPage({
    super.key,
    required this.title,
    required this.problems,
  });

  final String title;
  final List<dynamic> problems;

  @override
  State<MultipleChoiceProblemPage> createState() =>
      _MultipleChoiceProblemPageState();
}

class _MultipleChoiceProblemPageState extends State<MultipleChoiceProblemPage> {
  int _currentProblemIndex = 0;
  int? _selectedChoiceIndex;
  bool? _isCorrect;

  @override
  void initState() {
    super.initState();
    // The widget's 'problems' list can be used directly.
    // No need to load anything here.
  }

  void _checkAnswer(int selectedIndex) {
    setState(() {
      _selectedChoiceIndex = selectedIndex;
      _isCorrect =
          selectedIndex == widget.problems[_currentProblemIndex]['answer'];
    });
  }

  void _nextProblem() {
    setState(() {
      if (_currentProblemIndex < widget.problems.length - 1) {
        _currentProblemIndex++;
        _selectedChoiceIndex = null;
        _isCorrect = null;
      }
    });
  }

  void _previousProblem() {
    setState(() {
      if (_currentProblemIndex > 0) {
        _currentProblemIndex--;
        _selectedChoiceIndex = null;
        _isCorrect = null;
      }
    });
  }

  void _jumpToProblem(int index) {
    setState(() {
      if (index >= 0 && index < widget.problems.length) {
        _currentProblemIndex = index;
        _selectedChoiceIndex = null;
        _isCorrect = null;
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
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: widget.problems.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Question ${_currentProblemIndex + 1}/${widget.problems.length}',
                    style: Theme.of(context).textTheme.headlineSmall,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    widget.problems[_currentProblemIndex]['question'],
                    style: Theme.of(context).textTheme.bodyLarge,
                  ),
                  const SizedBox(height: 24),
                  ...(widget.problems[_currentProblemIndex]['choices']
                          as List<dynamic>)
                      .asMap()
                      .entries
                      .map((entry) {
                        int idx = entry.key;
                        String choice = entry.value;
                        Color? tileColor;
                        Icon? trailingIcon;
                        if (_selectedChoiceIndex == idx) {
                          if (_isCorrect!) {
                            tileColor = Colors.green.shade100;
                            trailingIcon = const Icon(
                              Icons.check_circle,
                              color: Colors.green,
                            );
                          } else {
                            tileColor = Colors.red.shade100;
                            trailingIcon = const Icon(
                              Icons.cancel,
                              color: Colors.red,
                            );
                          }
                        }

                        return Card(
                          color: tileColor,
                          child: ListTile(
                            title: Text(choice),
                            trailing: trailingIcon,
                            onTap: () => _checkAnswer(idx),
                          ),
                        );
                      }),
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
              onPressed: _currentProblemIndex > 0 ? _previousProblem : null,
            ),
            TextButton(
              child: const Text('Jump To'),
              onPressed: () => _showJumpToGrid(context),
            ),
            TextButton.icon(
              label: const Text('Next'),
              icon: const Icon(Icons.arrow_forward),
              onPressed: _currentProblemIndex < widget.problems.length - 1
                  ? _nextProblem
                  : null,
            ),
          ],
        ),
      ),
    );
  }
}
