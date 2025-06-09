import 'package:flutter/material.dart';
import 'package:learner/pages/subject_list_page.dart';

class DatasetListPage extends StatefulWidget {
  const DatasetListPage({super.key});

  @override
  State<DatasetListPage> createState() => _DatasetListPageState();
}

class _DatasetListPageState extends State<DatasetListPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Train yourself to be AI'),
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView(
              children: <Widget>[
                ListTile(
                  title: const Text('MMLU'),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) =>
                            const SubjectListPage(datasetName: 'MMLU'),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Center(child: Text('v0.0')),
          ),
        ],
      ),
    );
  }
} 