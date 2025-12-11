/**
 * Task Validator for Backlog.md
 *
 * Validates tasks before they're written to Backlog.md to prevent
 * silent parsing failures caused by malformed task data.
 *
 * Common issues this catches:
 * - [P] markers in titles (from flowspec)
 * - [US#] markers in titles
 * - T### prefixes in titles
 * - YAML-breaking characters in titles/filenames
 */

export interface BacklogTaskValidation {
  valid: boolean;
  errors: string[];
  warnings: string[];
  sanitizedTitle?: string;
}

export interface TaskInput {
  title: string;
  id?: string;
  status?: string;
  labels?: string[];
  description?: string;
}

interface ValidationPattern {
  pattern: RegExp;
  message: string;
  replacement: string;
}

/**
 * Patterns that break YAML parsing when present in task titles
 */
const YAML_BREAKING_PATTERNS: ValidationPattern[] = [
  {
    pattern: /\[P\]/gi,
    message: '[P] marker found - use "parallelizable" label instead',
    replacement: '',
  },
  {
    pattern: /\[US\d+\]/gi,
    message: '[US#] marker found - use label instead',
    replacement: '',
  },
  {
    pattern: /^T\d{3}\s*/i,
    message: 'T### prefix found - Backlog.md uses task-### format',
    replacement: '',
  },
  {
    pattern: /^\[.*?\]\s*/,
    message: 'Leading [...] found - will break YAML parsing',
    replacement: '',
  },
];

/**
 * Characters that are special in YAML and may cause parsing issues
 */
const YAML_SPECIAL_CHARS = /[:\[\]{}#&*!|>'"%@`]/;

/**
 * Valid status values for Backlog.md
 */
const VALID_STATUSES = ['To Do', 'In Progress', 'Done'];

/**
 * Validates a task for Backlog.md compatibility
 * Catches common issues that cause silent parsing failures
 *
 * @param task - The task to validate
 * @returns Validation result with errors, warnings, and sanitized title
 *
 * @example
 * const result = validateBacklogTask({ title: '[P] Add user authentication' });
 * if (!result.valid) {
 *   console.error('Task validation failed:', result.errors);
 *   console.log('Suggested title:', result.sanitizedTitle);
 * }
 */
export function validateBacklogTask(task: TaskInput): BacklogTaskValidation {
  const errors: string[] = [];
  const warnings: string[] = [];
  let sanitizedTitle = task.title;

  // Check for YAML-breaking characters in title
  for (const { pattern, message, replacement } of YAML_BREAKING_PATTERNS) {
    if (pattern.test(task.title)) {
      errors.push(`Title: ${message}`);
      sanitizedTitle = sanitizedTitle.replace(pattern, replacement).trim();
    }
  }

  // Check for unquoted special YAML characters
  if (YAML_SPECIAL_CHARS.test(sanitizedTitle) && !sanitizedTitle.startsWith('"')) {
    warnings.push('Title contains special characters - consider quoting it');
  }

  // Check title length
  if (sanitizedTitle.length === 0) {
    errors.push('Title is empty after sanitization');
  } else if (sanitizedTitle.length > 100) {
    warnings.push('Title is very long (>100 chars) - consider shortening');
  }

  // Validate ID format if provided
  if (task.id) {
    if (!/^task-\d{3}$/.test(task.id) && !/^task-\d+$/.test(task.id)) {
      warnings.push(`ID "${task.id}" doesn't match expected format (task-###)`);
    }
  }

  // Validate status
  if (task.status && !VALID_STATUSES.includes(task.status)) {
    warnings.push(`Status "${task.status}" may not be recognized. Valid: ${VALID_STATUSES.join(', ')}`);
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    sanitizedTitle: sanitizedTitle !== task.title ? sanitizedTitle : undefined,
  };
}

/**
 * Sanitizes a title for safe use in Backlog.md
 * Removes flowspec markers and ensures YAML compatibility
 *
 * @param title - The raw title to sanitize
 * @returns Sanitized title safe for Backlog.md
 *
 * @example
 * sanitizeTaskTitle('[P] [US1] Add feature') // Returns: 'Add feature'
 * sanitizeTaskTitle('T001 Setup project')    // Returns: 'Setup project'
 */
export function sanitizeTaskTitle(title: string): string {
  return title
    .replace(/\[P\]/gi, '')           // Remove [P] markers
    .replace(/\[US\d+\]/gi, '')       // Remove [US#] markers
    .replace(/^T\d{3}\s*/i, '')       // Remove T### prefix
    .replace(/^\[.*?\]\s*/, '')       // Remove any leading [...]
    .trim();
}

/**
 * Validates a task filename for Backlog.md
 *
 * @param filename - The filename to validate (e.g., "task-001 - Title.md")
 * @returns Validation result with errors and warnings
 *
 * @example
 * validateTaskFilename('task-011 - [P] Add feature.md')
 * // Returns: { valid: false, errors: ['Filename contains [ or ]...'] }
 */
export function validateTaskFilename(filename: string): BacklogTaskValidation {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Check for brackets in filename - these cause file system and parsing issues
  if (/\[|\]/.test(filename)) {
    errors.push('Filename contains [ or ] - these cause file system and parsing issues');
  }

  // Check format matches expected pattern
  const filenamePattern = /^task-(\d+) - (.+)\.md$/;
  const match = filename.match(filenamePattern);

  if (!match) {
    errors.push('Filename doesn\'t match expected format: "task-### - Title.md"');
  } else {
    const [, taskNum, title] = match;

    if (taskNum.length < 3) {
      warnings.push('Task number should be zero-padded (e.g., task-001)');
    }

    if (title.length > 50) {
      warnings.push('Title in filename is long - may cause issues on some systems');
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Extracts flowspec metadata from a task title and returns labels
 *
 * @param title - The title containing flowspec markers
 * @returns Object with sanitized title and extracted labels
 *
 * @example
 * extractFlowspecKitMetadata('[P] [US1] Add feature')
 * // Returns: { title: 'Add feature', labels: ['parallelizable', 'US1'] }
 */
export function extractFlowspecKitMetadata(title: string): {
  title: string;
  labels: string[];
} {
  const labels: string[] = [];

  // Extract [P] marker
  if (/\[P\]/i.test(title)) {
    labels.push('parallelizable');
  }

  // Extract [US#] markers
  const userStoryMatch = title.match(/\[US(\d+)\]/gi);
  if (userStoryMatch) {
    for (const match of userStoryMatch) {
      labels.push(match.replace(/[\[\]]/g, ''));
    }
  }

  return {
    title: sanitizeTaskTitle(title),
    labels,
  };
}

/**
 * Validates all task files in a directory
 * Useful for CI/CD pipelines or pre-commit hooks
 *
 * @param taskFiles - Array of task file info to validate
 * @returns Array of validation results for each file
 */
export function validateAllTasks(
  taskFiles: Array<{ filename: string; content: TaskInput }>
): Array<{ filename: string; validation: BacklogTaskValidation }> {
  return taskFiles.map(({ filename, content }) => {
    const filenameValidation = validateTaskFilename(filename);
    const contentValidation = validateBacklogTask(content);

    return {
      filename,
      validation: {
        valid: filenameValidation.valid && contentValidation.valid,
        errors: [...filenameValidation.errors, ...contentValidation.errors],
        warnings: [...filenameValidation.warnings, ...contentValidation.warnings],
        sanitizedTitle: contentValidation.sanitizedTitle,
      },
    };
  });
}
