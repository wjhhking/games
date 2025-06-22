import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/gpqa_experts_page.dart';
import 'package:learner/pages/multiple_choice_problem_page.dart';
import 'package:learner/widgets/dataset_intro_card.dart';

class GpqaPage extends StatefulWidget {
  const GpqaPage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<GpqaPage> createState() => _GpqaPageState();
}

class _GpqaPageState extends State<GpqaPage> {
  // These are the configurations downloaded from the GPQA dataset.
  final List<String> _configs = [
    'gpqa_main',
    'gpqa_extended',
    'gpqa_diamond',
    'gpqa_experts',
  ];

  final Map<String, String> _configDescriptions = {
    'gpqa_main': 'Core questions',
    'gpqa_extended': 'Extended question set',
    'gpqa_diamond': 'Diamond set',
    'gpqa_experts': 'About the domain experts',
  };

  Map<String, dynamic> _splitsInfo = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMetadata();
  }

  Future<void> _loadMetadata() async {
    try {
      final String path = 'data/gpqa/metadata.json';
      final String response = await rootBundle.loadString(path);
      final data = json.decode(response);
      if (mounted) {
        setState(() {
          _splitsInfo = data['splits_info'] ?? {};
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
      print("Error loading GPQA metadata: $e");
    }
  }

  Future<List<dynamic>> _loadAndTransformGpqa(String configName) async {
    final String path = 'data/gpqa/${configName}.json';
    final String response = await rootBundle.loadString(path);
    // The downloaded files are JSON Lines, so we need to split by line.
    final List<dynamic> originalProblems = response
        .split('\n')
        .where((line) => line.isNotEmpty)
        .map((line) => json.decode(line))
        .toList();

    final List<dynamic> transformedProblems = originalProblems.map((problem) {
      final String question =
          problem['Question'] ?? 'No question text provided.';
      List<String> choices;
      int answerIndex = -1;

      // Check for the format with keys 'A', 'B', 'C', 'D'
      if (problem.containsKey('A')) {
        choices = [
          problem['A'] ?? '',
          problem['B'] ?? '',
          problem['C'] ?? '',
          problem['D'] ?? '',
        ];
        switch (problem['Correct Answer'] ?? '') {
          case 'A':
            answerIndex = 0;
            break;
          case 'B':
            answerIndex = 1;
            break;
          case 'C':
            answerIndex = 2;
            break;
          case 'D':
            answerIndex = 3;
            break;
        }
      }
      // Check for the format with 'Correct Answer', 'Incorrect Answer 1', etc.
      else if (problem.containsKey('Correct Answer') &&
          problem.containsKey('Incorrect Answer 1')) {
        final String correctAnswerValue = problem['Correct Answer'];
        choices =
            [
                  correctAnswerValue,
                  problem['Incorrect Answer 1'],
                  problem['Incorrect Answer 2'],
                  problem['Incorrect Answer 3'],
                ]
                .where((c) => c != null) // Filter out potential nulls
                .map((c) => c.toString()) // Ensure all are strings
                .toList();

        // Shuffle the choices so the correct one isn't always first
        choices.shuffle();
        answerIndex = choices.indexOf(correctAnswerValue);
      }
      // Fallback for any unknown format
      else {
        choices = [];
      }

      return {'question': question, 'choices': choices, 'answer': answerIndex};
    }).toList();

    return transformedProblems;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.datasetInfo.name)),
      body: Column(
        children: [
          DatasetIntroCard(
            title: 'About ${widget.datasetInfo.name}',
            info: widget.datasetInfo.info,
            highestScore: widget.datasetInfo.highestScore,
          ),
          const Divider(height: 1),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _configs.length,
                    itemBuilder: (context, index) {
                      final configName = _configs[index];
                      final isExpertsConfig = configName == 'gpqa_experts';

                      final count = _splitsInfo[configName]?['train'] ?? 0;
                      final countText =
                          isExpertsConfig ? '$count Experts' : '$count Questions';
                      final description = _configDescriptions[configName] ?? '';

                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16.0,
                          vertical: 6.0,
                        ),
                        child: ListTile(
                          title: Text(configName),
                          subtitle: Text('$description • $countText'),
                          onTap: () async {
                            if (isExpertsConfig) {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => GpqaExpertsPage(
                                      datasetInfo: widget.datasetInfo),
                                ),
                              );
                            } else {
                              showDialog(
                                context: context,
                                barrierDismissible: false,
                                builder: (BuildContext context) {
                                  return const Center(
                                    child: CircularProgressIndicator(),
                                  );
                                },
                              );

                              final problems =
                                  await _loadAndTransformGpqa(configName);

                              Navigator.pop(context);

                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) =>
                                      MultipleChoiceProblemPage(
                                    title:
                                        '${widget.datasetInfo.name}: $configName',
                                    problems: problems,
                                  ),
                                ),
                              );
                            }
                          },
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
