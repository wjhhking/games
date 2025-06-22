import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/gsm8k_problem_page.dart';
import 'package:learner/widgets/dataset_intro_card.dart';

class Gsm8kPage extends StatefulWidget {
  const Gsm8kPage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<Gsm8kPage> createState() => _Gsm8kPageState();
}

class _Gsm8kPageState extends State<Gsm8kPage> {
  Map<String, dynamic> _metadata = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMetadata();
  }

  Future<void> _loadMetadata() async {
    try {
      final String path = 'data/gsm8k/metadata.json';
      final String response = await rootBundle.loadString(path);
      final data = json.decode(response);
      if (mounted) {
        setState(() {
          _metadata = data;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
      print("Error loading GSM8K metadata: $e");
    }
  }

  Future<void> _navigateToSplit(String splitName) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return const Dialog(
          child: Padding(
            padding: EdgeInsets.all(20.0),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(),
                SizedBox(width: 20),
                Text("Loading problems..."),
              ],
            ),
          ),
        );
      },
    );

    try {
      final String path = 'data/gsm8k/gsm8k_${splitName}.json';
      final String response = await rootBundle.loadString(path);
      final List<dynamic> problems = response.split('\n')
          .where((line) => line.isNotEmpty)
          .map((line) => json.decode(line))
          .toList();

      Navigator.pop(context); // Dismiss the loading dialog

      if (problems.isNotEmpty && mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => Gsm8kProblemPage(problems: problems),
          ),
        );
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No problems found for this split.')),
        );
      }
    } catch (e) {
      Navigator.pop(context); // Dismiss the loading dialog
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading problems for $splitName.')),
        );
      }
      print("Error loading GSM8K problems for $splitName: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    final splits = _metadata['splits'] as Map<String, dynamic>? ?? {};
    final splitNames = splits.keys.toList();

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
                    itemCount: splitNames.length,
                    itemBuilder: (context, index) {
                      final splitName = splitNames[index];
                      final problemCount = splits[splitName];

                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16.0,
                          vertical: 6.0,
                        ),
                        child: ListTile(
                          title: Text(splitName),
                          subtitle: Text('$problemCount problems'),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                          ),
                          onTap: () {
                            _navigateToSplit(splitName);
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
