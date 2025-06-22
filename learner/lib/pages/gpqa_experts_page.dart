import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:learner/data/datasets.dart';

class GpqaExpertsPage extends StatefulWidget {
  const GpqaExpertsPage({super.key, required this.datasetInfo});

  final DatasetInfo datasetInfo;

  @override
  State<GpqaExpertsPage> createState() => _GpqaExpertsPageState();
}

class _GpqaExpertsPageState extends State<GpqaExpertsPage> {
  List<dynamic> _experts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadExperts();
  }

  Future<void> _loadExperts() async {
    try {
      final String path = 'data/gpqa/gpqa_experts.json';
      final String response = await rootBundle.loadString(path);
      final List<dynamic> experts = response
          .split('\n')
          .where((line) => line.isNotEmpty)
          .map((line) => json.decode(line))
          .toList();

      if (mounted) {
        setState(() {
          _experts = experts;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
      print("Error loading GPQA experts: $e");
    }
  }

  String _formatDomain(String domainString) {
    return domainString
        .replaceAll(RegExp(r"[\[\]']"), '')
        .trim();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('GPQA Experts')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: _experts.length,
              itemBuilder: (context, index) {
                final expert = _experts[index];
                return Card(
                  margin:
                      const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _formatDomain(expert['Domain'] ?? 'N/A'),
                          style: Theme.of(context)
                              .textTheme
                              .titleMedium
                              ?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          expert['Description of Expertise'] ?? 'No description.',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 12),
                        const Divider(height: 1),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            _buildStat(
                              context,
                              'Qualification',
                              expert['Qualifications']
                                  ?.replaceAll(RegExp(r"[\[\]']"), ''),
                            ),
                            _buildStat(
                              context,
                              'Expert Accuracy',
                              '${((expert['Expert Accuracy'] ?? 0.0) * 100).toStringAsFixed(0)}%',
                            ),
                          ],
                        )
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }

  Widget _buildStat(BuildContext context, String label, String? value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall,
        ),
        Text(
          value ?? 'N/A',
          style: Theme.of(context)
              .textTheme
              .bodyMedium
              ?.copyWith(fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
} 