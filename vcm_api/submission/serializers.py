from rest_framework import serializers
from vcm_api.submission.models import Submission
from vcm_api.problem.models import Problem
from django.contrib.auth import get_user_model
from vcm_api.online_judge import codechef, codeforces, atcoder
from vcm_api.user.serializers import UserSerializer
from vcm_api.problem.serializers import ProblemSerializer
from datetime import datetime
import pytz


class SubmissionSerializer(serializers.ModelSerializer):
    User = get_user_model()

    class Meta:
        model = Submission
        fields = []

    def create(self, validated_data):
        current_user = self.context['request'].user
        if self.context['request'].data['problem_id'] is None:
            raise serializers.ValidationError(detail="problem id field is required")

        problem_id = self.context['request'].data['problem_id']

        required_problem = Problem.objects.filter(id=problem_id).first()
        if required_problem is None:
            raise serializers.ValidationError(detail="problem id is incorrect")
        required_online_judge = required_problem.online_judge
        required_contest = required_problem.contest

        solved_status = False

        if required_online_judge == "codeforces":
            codeforces_username = current_user.profile.cf_handle
            if codeforces_username is None:
                raise serializers.ValidationError(detail="codeforces handle is not available")

            required_problem_id = codeforces.get_problem_id(
                codeforces.convert_problem_url(required_problem.link))
            required_contest_starttime = datetime.timestamp(required_contest.start_date_time)
            required_contest_duration = required_contest.duration.total_seconds()
            solved_status = codeforces.check_solved(
                codeforces_username,
                required_problem_id,
                required_contest_starttime,
                required_contest_duration)

        elif required_online_judge == "codechef":
            codechef_username = current_user.profile.cc_handle
            if codechef_username is None:
                raise serializers.ValidationError(detail="codechef handle is not available")

            instance_codechef = codechef.Codechef()
            required_problem_id = instance_codechef.get_problem_id(required_problem.link)
            required_contest_starttime = datetime.timestamp(required_contest.start_date_time)
            required_contest_duration = required_contest.duration.total_seconds()
            solved_status = instance_codechef.check_solved(
                codechef_username,
                required_problem_id,
                required_contest_starttime,
                required_contest_duration)

        else:
            atcoder_username = current_user.profile.ac_handle
            if atcoder_username is None:
                raise serializers.ValidationError(detail="atcoder handle is not available")
            required_problem_id = atcoder.get_problem_id(required_problem.link)
            required_contest_starttime = datetime.timestamp(required_contest.start_date_time)
            required_contest_duration = required_contest.duration.total_seconds()
            solved_status = atcoder.check_solved(
                atcoder_username,
                required_problem_id,
                int(required_contest_starttime),
                int(required_contest_duration))

        if solved_status is False:
            raise serializers.ValidationError(detail="problem is not solved")

        existing_submission = Submission.objects.filter(
            problem=required_problem, correct_answer=True).first()

        if existing_submission is not None:
            raise serializers.ValidationError(detail="problem is already solved")

        new_submission = Submission.objects.create(
            user=current_user,
            problem=required_problem,
            time=datetime.now(pytz.UTC),
            correct_answer=True)
        return new_submission


class SubmissionListSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    user = UserSerializer()

    class Meta:
        model = Submission
        fields = ['id', 'user', 'problem', 'correct_answer', 'time']
