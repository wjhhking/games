import 'package:flutter/material.dart';

class SweBenchProblemPage extends StatefulWidget {
  final List<dynamic> problems;
  final int startingIndex;
  final String pageTitle;

  const SweBenchProblemPage({
    super.key,
    required this.problems,
    this.startingIndex = 0,
    required this.pageTitle,
  });

  @override
  State<SweBenchProblemPage> createState() => _SweBenchProblemPageState();
}

class _SweBenchProblemPageState extends State<SweBenchProblemPage>
    with SingleTickerProviderStateMixin {
  late int _currentIndex;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.startingIndex;
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _nextProblem() {
    if (_currentIndex < widget.problems.length - 1) {
      setState(() {
        _currentIndex++;
        _tabController.index = 0;
      });
    }
  }

  void _previousProblem() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
        _tabController.index = 0;
      });
    }
  }

  void _jumpToProblem(int index) {
    setState(() {
      if (index >= 0 && index < widget.problems.length) {
        _currentIndex = index;
        _tabController.index = 0;
      }
    });
  }

  void _showJumpToGrid(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext context) {
        return GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 5,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
          ),
          itemCount: widget.problems.length,
          itemBuilder: (context, index) {
            return ElevatedButton(
              onPressed: () {
                _jumpToProblem(index);
                Navigator.pop(context);
              },
              child: FittedBox(
                fit: BoxFit.scaleDown,
                child: Text('${index + 1}'),
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final problem = widget.problems[_currentIndex];
    final problemStatement = problem['problem_statement']?.toString() ?? 'No problem statement available.';
    final patch = problem['patch']?.toString() ?? 'No patch available.';
    final instanceId = problem['instance_id']?.toString() ?? 'N/A';

    return Scaffold(
      appBar: AppBar(
        title: Text(
            '${widget.pageTitle} - Problem ${_currentIndex + 1} of ${widget.problems.length}'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Problem'),
            Tab(text: 'Solution Patch'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          // Problem Statement Tab
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Instance ID: $instanceId', style: Theme.of(context).textTheme.bodySmall),
                const SizedBox(height: 8),
                SelectableText(problemStatement),
              ],
            ),
          ),
          // Patch Tab
          SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: SelectableText(patch),
          ),
        ],
      ),
      bottomNavigationBar: BottomAppBar(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            TextButton.icon(
              icon: const Icon(Icons.arrow_back),
              label: const Text('Previous'),
              onPressed: _currentIndex > 0 ? _previousProblem : null,
            ),
            TextButton(
              child: const Text('Jump To'),
              onPressed: () => _showJumpToGrid(context),
            ),
            TextButton.icon(
              icon: const Icon(Icons.arrow_forward),
              label: const Text('Next'),
              onPressed: _currentIndex < widget.problems.length - 1
                  ? _nextProblem
                  : null,
            ),
          ],
        ),
      ),
    );
  }
} 