import 'package:flutter/material.dart';
import 'package:flutter_math_fork/flutter_math.dart';

/// A private helper widget that renders inline content, including plain text,
/// inline math ($...$), and math-like words (e.g., with _, ^, \).
class _InlineContent extends StatelessWidget {
  const _InlineContent(this.text, {this.style});

  final String text;
  final TextStyle? style;

  @override
  Widget build(BuildContext context) {
    // This tokenizer regex finds math expressions and leaves the rest as plain text.
    final tokenizer = RegExp(r'(\$.*?\$)|(\S*[_^\\]\S*)');

    final List<Widget> widgets = [];
    int currentPos = 0;

    for (final match in tokenizer.allMatches(text)) {
      // Add the plain text part before the current match.
      if (match.start > currentPos) {
        widgets.add(
          SelectableText(text.substring(currentPos, match.start), style: style),
        );
      }

      // Extract and add the math part as a separate widget.
      String mathContent;
      if (match.group(1) != null) {
        // Delimited: $...$
        mathContent = match.group(1)!.substring(1, match.group(1)!.length - 1);
      } else {
        // Heuristic: math-like word
        mathContent = match.group(2)!;
      }
      
      final mathWidget = Math.tex(
        mathContent,
        mathStyle: MathStyle.text,
        textStyle: style,
      );

      // Heuristic to detect potentially wide elements and make them scrollable.
      if (mathContent.contains(r'\') || mathContent.length > 20) {
        widgets.add(SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: mathWidget,
        ));
      } else {
        widgets.add(mathWidget);
      }

      currentPos = match.end;
    }

    // Add any plain text left at the end of the string.
    if (currentPos < text.length) {
      widgets.add(SelectableText(text.substring(currentPos), style: style));
    }

    // Use a Wrap layout to arrange the Text and Math widgets like words in a
    // paragraph, which avoids the baseline alignment errors.
    return Wrap(
      crossAxisAlignment: WrapCrossAlignment.center,
      alignment: WrapAlignment.start,
      children: widgets,
    );
  }
}

/// A widget that intelligently renders a string with a mix of plain text and
/// TeX math expressions. It distinguishes between block-level display math
/// and inline content to prevent layout errors.
class MixedTextMath extends StatelessWidget {
  const MixedTextMath(this.text, {super.key, this.style});

  final String text;
  final TextStyle? style;

  @override
  Widget build(BuildContext context) {
    // Regex to split the text by display math blocks (\[...\]).
    final displayMathRegExp = RegExp(r'(\\\[.*?\\\])', dotAll: true);

    final List<Widget> children = [];
    int currentPos = 0;

    for (final match in displayMathRegExp.allMatches(text)) {
      // Add the section of inline content that came before this display block.
      if (match.start > currentPos) {
        children.add(
          _InlineContent(text.substring(currentPos, match.start), style: style),
        );
      }

      // Extract the math content from the display block, stripping delimiters.
      final mathContent = match
          .group(0)!
          .substring(2, match.group(0)!.length - 2);

      // Add the display math block, wrapped in a horizontal scroller.
      children.add(
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Math.tex(
            mathContent,
            mathStyle: MathStyle.display,
            textStyle: style,
          ),
        ),
      );

      currentPos = match.end;
    }

    // Add any final inline content that came after the last display block.
    if (currentPos < text.length) {
      children.add(_InlineContent(text.substring(currentPos), style: style));
    }

    if (children.isEmpty) {
      // If there was no display math, the whole string is inline content.
      return _InlineContent(text, style: style);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: children,
    );
  }
} 