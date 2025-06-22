import 'package:flutter/material.dart';

class DatasetInfo {
  final String name;
  final String highestScore;
  final String info;
  final String? label;

  const DatasetInfo({
    required this.name,
    required this.highestScore,
    required this.info,
    this.label,
  });
}

/// A centralized map of all dataset information.
final Map<String, DatasetInfo> datasetInfoMap = {
  'MMLU': const DatasetInfo(
    name: 'MMLU',
    highestScore: '>90% (many models)',
    info:
        'A diverse range of college-level subjects. The leading benchmark pre-2024, slightly outdated due to rapid development and data contamination.',
    label: 'College',
  ),
  'GPQA': const DatasetInfo(
    name: 'GPQA',
    highestScore: '86.4% (Gemini 2.5)',
    info:
        'A Graduate-Level Google-Proof Q&A Benchmark, meaning results can not be found even with Google. The "diamond" subset is considered state-of-the-art, with best performance from Gemini.',
    label: 'Ph.D.',
  ),
  'HLE': const DatasetInfo(
    name: 'HLE',
    highestScore: '21.6% (Gemini 2.5)',
    info:
        "Humanity's Last Exam (HLE) is a multi-modal benchmark at the frontier of human knowledge. The author has to say it is absolutely insane and too f***ing hard.",
    label: 'Einstein',
  ),
  'GSM8K': const DatasetInfo(
    name: 'GSM8K',
    highestScore: '>97% (many models)',
    info:
        'Grade school math word problems, which was hard for AI models prior to 2023.',
    label: 'Grade school',
  ),
  'MATH': const DatasetInfo(
    name: 'MATH',
    highestScore: '>60% (?)',
    info:
        'A benchmark of mathematics problems with diver difficulty levels, ranging from high school to Olympiad. While a good portion of the problems are solvable by AI, the author has to say it is still a good benchmark for AI.',
    label: 'High school',
  ),
  'AIME': const DatasetInfo(
    name: 'AIME',
    highestScore: '87% (O3)',
    info:
        'The American Invitational Mathematics Examination (AIME) is a qualifying exam for the USA team for the International Mathematical Olympiad (IMO).',
    label: 'Olympiad',
  ),
  'SWE-bench': const DatasetInfo(
    name: 'SWE-bench',
    highestScore: '72.7% (Claude 4)',
    info: 'A benchmark for software engineering tasks.',
    label: 'Google L4',
  ),
};
