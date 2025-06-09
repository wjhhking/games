import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class ProblemPage extends StatefulWidget {
  const ProblemPage({
    super.key,
    required this.subjectId,
    required this.subjectName,
  });

  final String subjectId;
  final String subjectName;

  @override
  State<ProblemPage> createState() => _ProblemPageState();
}

class _ProblemPageState extends State<ProblemPage> {
  List<dynamic> _problems = [];
  int _currentProblemIndex = 0;
  int? _selectedChoiceIndex;
  bool? _isCorrect;

  @override
  void initState() {
    super.initState();
    _loadProblems();
  }

  Future<void> _loadProblems() async {
    final String response =
        await rootBundle.loadString('data/mmlu/${widget.subjectId}.json');
    final data = await json.decode(response);
    setState(() {
      _problems = data;
    });
  }

  void _checkAnswer(int selectedIndex) {
    setState(() {
      _selectedChoiceIndex = selectedIndex;
      _isCorrect = selectedIndex == _problems[_currentProblemIndex]['answer'];
    });
  }

  void _nextProblem() {
    setState(() {
      if (_currentProblemIndex < _problems.length - 1) {
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
      if (index >= 0 && index < _problems.length) {
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
          itemCount: _problems.length,
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
      appBar: AppBar(
        title: Text(widget.subjectName),
      ),
      body: _problems.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Question ${_currentProblemIndex + 1}/${_problems.length}',
                    style: Theme.of(context).textTheme.headlineSmall,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    _problems[_currentProblemIndex]['question'],
                    style: Theme.of(context).textTheme.bodyLarge,
                  ),
                  const SizedBox(height: 24),
                  ...(_problems[_currentProblemIndex]['choices']
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
                        trailingIcon = const Icon(Icons.check_circle,
                            color: Colors.green);
                      } else {
                        tileColor = Colors.red.shade100;
                        trailingIcon =
                            const Icon(Icons.cancel, color: Colors.red);
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
              onPressed:
                  _currentProblemIndex > 0 ? _previousProblem : null,
            ),
            TextButton(
              child: const Text('Jump To'),
              onPressed: () => _showJumpToGrid(context),
            ),
            TextButton.icon(
              label: const Text('Next'),
              icon: const Icon(Icons.arrow_forward),
              onPressed: _currentProblemIndex < _problems.length - 1
                  ? _nextProblem
                  : null,
            ),
          ],
        ),
      ),
    );
  }
} 