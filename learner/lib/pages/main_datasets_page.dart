import 'package:flutter/material.dart';
import 'package:learner/data/datasets.dart';
import 'package:learner/pages/aime_page.dart';
import 'package:learner/pages/gpqa_page.dart';
import 'package:learner/pages/gsm8k_page.dart';
import 'package:learner/pages/hle_page.dart';
import 'package:learner/pages/math_page.dart';
import 'package:learner/pages/mmlu_subjects_page.dart';
import 'package:learner/pages/swe_bench_page.dart';

class MainDatasetsPage extends StatefulWidget {
  const MainDatasetsPage({super.key});

  @override
  State<MainDatasetsPage> createState() => _MainDatasetsPageState();
}

class _MainDatasetsPageState extends State<MainDatasetsPage> {
  final List<String> _datasetNames = datasetInfoMap.keys.toList();

  Widget? _getPageForDataset(String name) {
    final info = datasetInfoMap[name];
    if (info == null) return null;

    switch (name) {
      case 'MMLU':
        return MMLUSubjectsPage(datasetInfo: info);
      case 'GPQA':
        return GpqaPage(datasetInfo: info);
      case 'HLE':
        return HlePage(datasetInfo: info);
      case 'GSM8K':
        return Gsm8kPage(datasetInfo: info);
      case 'MATH':
        return MathPage(datasetInfo: info);
      case 'AIME':
        return AimePage(datasetInfo: info);
      case 'SWE-bench':
        return SweBenchPage(datasetInfo: info);
      default:
        return null; // For 'Coming soon' datasets
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('What can AI do?'),
      ),
      body: Column(
        children: <Widget>[
          Card(
            margin: const EdgeInsets.all(16.0),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Text(
                    'How smart is AI now?',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Get a direct feeling of the difficulty levels.',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Colors.grey[700],
                        ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Below are the common tests used for evaluating LLMs,\n ranging from college-level to Einstein-level (HLE).',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "HLE, Humanity's Last Exam, is considered the hardest problems on Earth, that you should see for yourself.",
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(vertical: 8.0),
              itemCount: _datasetNames.length,
              itemBuilder: (context, index) {
                final datasetName = _datasetNames[index];
                final dataset = datasetInfoMap[datasetName]!;
                return Card(
                  margin: const EdgeInsets.symmetric(
                    horizontal: 16.0,
                    vertical: 6.0,
                  ),
                  child: InkWell(
                    onTap: () {
                      final page = _getPageForDataset(dataset.name);
                      if (page != null) {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => page),
                        );
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Coming soon!'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      }
                    },
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16.0, vertical: 12.0),
                      child: Row(
                        children: <Widget>[
                          Expanded(
                            flex: 3,
                            child: Text(
                              dataset.name,
                              style:
                                  const TextStyle(fontWeight: FontWeight.w500),
                            ),
                          ),
                          Expanded(
                            flex: 3,
                            child: dataset.label != null
                                ? Text(
                                    dataset.label!,
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      fontStyle: FontStyle.italic,
                                      color: Theme.of(context)
                                          .textTheme
                                          .bodySmall
                                          ?.color,
                                    ),
                                  )
                                : const SizedBox(),
                          ),
                          Expanded(
                            flex: 4,
                            child: Text(
                              dataset.highestScore,
                              textAlign: TextAlign.right,
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ),
                          const SizedBox(width: 10),
                          const Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                            color: Colors.grey,
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Center(child: Text('v0.1 by June 20, 2025')),
          ),
        ],
      ),
    );
  }
}
