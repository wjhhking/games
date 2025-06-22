import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/multiple_choice_problem_page.dart';
import 'package:learner/widgets/dataset_intro_card.dart';

class MMLUSubjectsPage extends StatefulWidget {
  const MMLUSubjectsPage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<MMLUSubjectsPage> createState() => _MMLUSubjectsPageState();
}

class _MMLUSubjectsPageState extends State<MMLUSubjectsPage> {
  List<dynamic> _subjects = [];
  int _totalProblems = 0;

  @override
  void initState() {
    super.initState();
    _loadSubjects();
  }

  Future<void> _loadSubjects() async {
    final String response = await rootBundle.loadString(
      'data/mmlu/subjects.json',
    );
    final data = await json.decode(response);
    int total = 0;
    for (var subject in data) {
      total += (subject['count'] as int?) ?? 0;
    }
    setState(() {
      _subjects = data;
      _totalProblems = total;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('${widget.datasetInfo.name} Subjects')),
      body: Column(
        children: [
          DatasetIntroCard(
            title: 'About ${widget.datasetInfo.name}',
            info: widget.datasetInfo.info,
            highestScore: widget.datasetInfo.highestScore,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Text(
              '${_subjects.length} subjects with $_totalProblems total problems.',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: ListView.builder(
              itemCount: _subjects.length,
              itemBuilder: (context, index) {
                return Card(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 16.0,
                    vertical: 6.0,
                  ),
                  child: ListTile(
                    title: Text(_subjects[index]['name']),
                    subtitle: Text('Questions: ${_subjects[index]['count']}'),
                    onTap: () async {
                      final String response = await rootBundle.loadString(
                        'data/mmlu/${_subjects[index]['id']}.json',
                      );
                      final List<dynamic> problems = await json.decode(
                        response,
                      );
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => MultipleChoiceProblemPage(
                            title: _subjects[index]['name'],
                            problems: problems,
                          ),
                        ),
                      );
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
