import 'package:flutter/material.dart';

class DatasetIntroCard extends StatelessWidget {
  const DatasetIntroCard({
    super.key,
    required this.title,
    required this.info,
    required this.highestScore,
  });

  final String title;
  final String info;
  final String highestScore;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16.0),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 12.0),
            Text.rich(
              TextSpan(
                style: Theme.of(context).textTheme.bodyLarge,
                children: [
                  const TextSpan(
                    text: 'Info: ',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  TextSpan(text: info),
                ],
              ),
            ),
            const SizedBox(height: 8.0),
            Text.rich(
              TextSpan(
                style: Theme.of(context).textTheme.bodyLarge,
                children: [
                  const TextSpan(
                    text: 'Highest Score: ',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  TextSpan(text: highestScore),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
