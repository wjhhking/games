import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/pages/problem_page.dart';

class SubjectListPage extends StatefulWidget {
  const SubjectListPage({super.key, required this.datasetName});

  final String datasetName;

  @override
  State<SubjectListPage> createState() => _SubjectListPageState();
}

class _SubjectListPageState extends State<SubjectListPage> {
  List<dynamic> _subjects = [];

  @override
  void initState() {
    super.initState();
    _loadSubjects();
  }

  Future<void> _loadSubjects() async {
    final String response =
        await rootBundle.loadString('data/mmlu/subjects.json');
    final data = await json.decode(response);
    setState(() {
      _subjects = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.datasetName} Subjects'),
      ),
      body: ListView.builder(
        itemCount: _subjects.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(_subjects[index]['name']),
            subtitle: Text('Questions: ${_subjects[index]['count']}'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ProblemPage(
                    subjectId: _subjects[index]['id'],
                    subjectName: _subjects[index]['name'],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
} 