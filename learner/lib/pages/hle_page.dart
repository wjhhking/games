import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/hle_problem_page.dart';
import 'package:learner/widgets/dataset_intro_card.dart';

class HlePage extends StatefulWidget {
  const HlePage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<HlePage> createState() => _HlePageState();
}

class _HlePageState extends State<HlePage> {
  List<dynamic> _categories = [];
  bool _isLoading = true;
  int _totalProblems = 0;

  @override
  void initState() {
    super.initState();
    _loadHleCategories();
  }

  String _sanitizeCategoryForFilename(String name) {
    // This sanitization logic must match the Python script that created the files.
    // It removes any character that is not a letter or a number.
    return name.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '');
  }

  Future<void> _navigateToCategory(
    String categoryName,
    String categoryFile,
  ) async {
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
      final String path = 'data/hle/$categoryFile';
      final String response = await rootBundle.loadString(path);
      final List<dynamic> problems = json.decode(response);

      Navigator.pop(context); // Dismiss the loading dialog

      if (problems.isNotEmpty && mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) =>
                HleProblemPage(problems: problems, startingIndex: 0),
          ),
        );
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('No problems found for this category.')),
        );
      }
    } catch (e) {
      Navigator.pop(context); // Dismiss the loading dialog
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Error loading problems for ${widget.datasetInfo.name}.',
            ),
          ),
        );
      }
      print("Error loading HLE problems for ${widget.datasetInfo.name}: $e");
    }
  }

  Future<void> _loadHleCategories() async {
    try {
      final String path = 'data/hle/metadata.json';
      final String response = await rootBundle.loadString(path);
      final data = json.decode(response);
      if (mounted) {
        setState(() {
          _categories = data['categories'];
          _totalProblems = data['total_problems'];
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
      print("Error loading HLE metadata: $e");
    }
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
          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: 16.0,
              vertical: 8.0,
            ),
            child: Text(
              _isLoading
                  ? 'Loading categories...'
                  : '${_categories.length} categories with $_totalProblems total problems.',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _categories.length,
                    itemBuilder: (context, index) {
                      final category = _categories[index];
                      final categoryName = category['name'];
                      final problemCount = category['count'];
                      final categoryFile =
                          '${_sanitizeCategoryForFilename(categoryName)}.json';

                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16.0,
                          vertical: 6.0,
                        ),
                        child: ListTile(
                          title: Text(categoryName),
                          subtitle: Text('$problemCount problems'),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                          ),
                          onTap: () {
                            _navigateToCategory(categoryName, categoryFile);
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
