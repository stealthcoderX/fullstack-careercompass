-- ============================================================================
-- CareerCompass MySQL Query Examples
-- Made by stealthcoderX | All rights reserved.
-- ============================================================================

-- See all users
SELECT * FROM users;

-- See how many users registered
SELECT COUNT(*) as total_users FROM users;

-- See user who took the quiz
SELECT id, name, email, predicted_career FROM users WHERE predicted_career IS NOT NULL;

-- See latest user
SELECT * FROM users ORDER BY created_at DESC LIMIT 1;

-- See user's quiz scores
SELECT id, name, email, score_json FROM users WHERE score_json IS NOT NULL;