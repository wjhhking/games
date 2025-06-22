import 'package:flutter/material.dart';
import 'package:flutter_math_fork/flutter_math.dart';

/// A private helper widget that renders inline content, including plain text,
/// inline math ($...$), and math-like words (e.g., with _, ^, \).
class _InlineContent extends StatelessWidget {
  const _InlineContent(this.text, {this.style});

  final String text;
  final TextStyle? style;

  @override
  Widget build(BuildContext context) {
    // This tokenizer regex finds math expressions and leaves the rest as plain text.
    final tokenizer = RegExp(r'(\$.*?\$)|(\S*[_^\\]\S*)');

    final List<Widget> widgets = [];
    int currentPos = 0;

    for (final match in tokenizer.allMatches(text)) {
      // Add the plain text part before the current match.
      if (match.start > currentPos) {
        widgets.add(
          SelectableText(text.substring(currentPos, match.start), style: style),
        );
      }

      // Extract and add the math part as a separate widget.
      String mathContent;
      if (match.group(1) != null) {
        // Delimited: $...$
        mathContent = match.group(1)!.substring(1, match.group(1)!.length - 1);
      } else {
        // Heuristic: math-like word
        mathContent = match.group(2)!;
      }
      widgets.add(
        Math.tex(mathContent, mathStyle: MathStyle.text, textStyle: style),
      );

      currentPos = match.end;
    }

    // Add any plain text left at the end of the string.
    if (currentPos < text.length) {
      widgets.add(SelectableText(text.substring(currentPos), style: style));
    }

    // Use a Wrap layout to arrange the Text and Math widgets like words in a
    // paragraph, which avoids the baseline alignment errors.
    return Wrap(
      crossAxisAlignment: WrapCrossAlignment.center,
      alignment: WrapAlignment.start,
      children: widgets,
    );
  }
}

/// A widget that intelligently renders a string with a mix of plain text and
/// TeX math expressions. It distinguishes between block-level display math
/// and inline content to prevent layout errors.
class MixedTextMath extends StatelessWidget {
  const MixedTextMath(this.text, {super.key, this.style});

  final String text;
  final TextStyle? style;

  @override
  Widget build(BuildContext context) {
    // Regex to split the text by display math blocks (\[...\]).
    final displayMathRegExp = RegExp(r'(\\\[.*?\\\])', dotAll: true);

    final List<Widget> children = [];
    int currentPos = 0;

    for (final match in displayMathRegExp.allMatches(text)) {
      // Add the section of inline content that came before this display block.
      if (match.start > currentPos) {
        children.add(
          _InlineContent(text.substring(currentPos, match.start), style: style),
        );
      }

      // Extract the math content from the display block, stripping delimiters.
      final mathContent = match
          .group(0)!
          .substring(2, match.group(0)!.length - 2);

      // Add the display math block, wrapped in a horizontal scroller.
      children.add(
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Math.tex(
            mathContent,
            mathStyle: MathStyle.display,
            textStyle: style,
          ),
        ),
      );

      currentPos = match.end;
    }

    // Add any final inline content that came after the last display block.
    if (currentPos < text.length) {
      children.add(_InlineContent(text.substring(currentPos), style: style));
    }

    if (children.isEmpty) {
      // If there was no display math, the whole string is inline content.
      return _InlineContent(text, style: style);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: children,
    );
  }
}

class HleProblemPage extends StatefulWidget {
  const HleProblemPage({
    super.key,
    required this.problems,
    required this.startingIndex,
  });

  final List<dynamic> problems;
  final int startingIndex;

  @override
  State<HleProblemPage> createState() => _HleProblemPageState();
}

class _HleProblemPageState extends State<HleProblemPage> {
  late int _currentProblemIndex;
  bool _showAnswer = false;

  @override
  void initState() {
    super.initState();
    _currentProblemIndex = widget.startingIndex;
  }

  void _nextProblem() {
    if (_currentProblemIndex < widget.problems.length - 1) {
      setState(() {
        _currentProblemIndex++;
        _showAnswer = false;
      });
    }
  }

  void _previousProblem() {
    if (_currentProblemIndex > 0) {
      setState(() {
        _currentProblemIndex--;
        _showAnswer = false;
      });
    }
  }

  void _jumpToProblem(int index) {
    if (index >= 0 && index < widget.problems.length) {
      setState(() {
        _currentProblemIndex = index;
        _showAnswer = false;
      });
    }
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

  Widget _buildProblemContent(Map<String, dynamic> problem) {
    final String questionText = problem['question'] ?? 'No question text.';
    final String? imagePath = problem['image_preview'] != null
        ? 'data/hle/${problem['image_preview']}'
        : null;

    String questionPart = questionText;
    List<String> answerChoices = [];

    if (questionText.contains('Answer Choices:')) {
      final parts = questionText.split('Answer Choices:');
      questionPart = parts[0].trim();
      answerChoices = parts[1].trim().split('\n').map((e) => e.trim()).toList();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        MixedTextMath(
          questionPart,
          style: Theme.of(context).textTheme.headlineSmall,
        ),
        if (answerChoices.isNotEmpty) ...[
          const SizedBox(height: 16),
          Text(
            'Answer Choices:',
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          ...answerChoices.map(
            (choice) => Padding(
              padding: const EdgeInsets.only(bottom: 8.0),
              child: MixedTextMath(
                choice,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ),
          ),
        ],
        const SizedBox(height: 16),
        if (imagePath != null)
          Center(
            child: Image.asset(
              imagePath,
              frameBuilder: (context, child, frame, wasSynchronouslyLoaded) {
                if (wasSynchronouslyLoaded) return child;
                return AnimatedOpacity(
                  opacity: frame == null ? 0 : 1,
                  duration: const Duration(seconds: 1),
                  curve: Curves.easeOut,
                  child: child,
                );
              },
              errorBuilder: (context, error, stackTrace) {
                return const Icon(
                  Icons.error_outline,
                  color: Colors.red,
                  size: 50,
                );
              },
            ),
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> currentProblem =
        widget.problems[_currentProblemIndex];

    return Scaffold(
      appBar: AppBar(title: Text('HLE Problem ${_currentProblemIndex + 1}')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildProblemContent(currentProblem),
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
            if (_showAnswer) ...[
              const SizedBox(height: 24),
              const Divider(),
              const SizedBox(height: 16),
              Text('Answer:', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 8),
              MixedTextMath(
                currentProblem['answer'] ?? 'No answer provided.',
                style: Theme.of(
                  context,
                ).textTheme.bodyLarge?.copyWith(fontStyle: FontStyle.italic),
              ),
              const SizedBox(height: 24),
              Text('Rationale:', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 8),
              MixedTextMath(
                currentProblem['rationale'] ?? 'No rationale provided.',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ],
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: _currentProblemIndex > 0 ? _previousProblem : null,
            ),
            TextButton(
              child: Text(
                '${_currentProblemIndex + 1} / ${widget.problems.length}',
              ),
              onPressed: () => _showJumpToGrid(context),
            ),
            IconButton(
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
