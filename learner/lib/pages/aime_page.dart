import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/aime_problem_page.dart';
import 'package:learner/widgets/dataset_intro_card.dart';

class AimePage extends StatefulWidget {
  const AimePage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<AimePage> createState() => _AimePageState();
}

class _AimePageState extends State<AimePage> {
  Map<String, dynamic> _metadata = {};
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMetadata();
  }

  Future<void> _loadMetadata() async {
    try {
      final String path = 'data/aime/metadata.json';
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
      print("Error loading AIME metadata: $e");
    }
  }

  Future<void> _navigateToConfig(String configName) async {
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
      final String path = 'data/aime/$configName/aime_${configName}_test.json';
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
            builder: (context) => AimeProblemPage(
              problems: problems,
              pageTitle: configName,
            ),
          ),
        );
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No problems found for this configuration.')),
        );
      }
    } catch (e) {
      Navigator.pop(context); // Dismiss the loading dialog
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading problems for $configName.')),
        );
      }
      print("Error loading AIME problems for $configName: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    final configs = _metadata['configs_downloaded'] as List<dynamic>? ?? [];

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
                    itemCount: configs.length,
                    itemBuilder: (context, index) {
                      final configName = configs[index] as String;
                      final problemCount = _metadata['splits_info']?[configName]?['test'] ?? 0;

                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16.0,
                          vertical: 6.0,
                        ),
                        child: ListTile(
                          title: Text(configName),
                          subtitle: Text('$problemCount problems'),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                          ),
                          onTap: () {
                            _navigateToConfig(configName);
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